from flask import Flask, jsonify, request, render_template
from database.db_context import DatabaseContext
from models.player import Player
from models.dealer import Dealer
from models.shoe import Shoe
from repositories.player_repository import PlayerRepository
from services.player_service import PlayerService

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_context = DatabaseContext("sqlite:///blackjack.sqlite3")
db_context.setup_database()
session_db = db_context.get_session()
repo = PlayerRepository(session_db)
player_service = PlayerService(repo)

current_game_state = {
    "player": None,
    "dealer": None,
    "shoe": None,
    "round_active": False,
    "active_hand_index": 0
}

def get_game_json():
    p = current_game_state["player"]
    d = current_game_state["dealer"]
    if not p or not d:
        return {"error" : "Game not started"}
    
    round_active = current_game_state["round_active"]
    active_idx = current_game_state["active_hand_index"]

    player_hands = []
    for i, hand in enumerate(p.hands):

        if round_active and i == active_idx:
            score_to_display = hand.display_score
        else:
            score_to_display = str(hand.score)

        player_hands.append({
            "cards": [str(card) for card in hand.cards],
            "score": score_to_display,
            "is_busted": hand.is_busted,
            "can_double": p.can_double_down(i),
            "can_split": p.can_split(i)
        })

    round_active = current_game_state["round_active"]

    if round_active and len(d.hand.cards) >= 2:
        dealer_cards = [str(d.hand.cards[0]), "🂠"]
        dealer_score = 11 if d.hand.cards[0].rank == 'A' else d.hand.cards[0].value
    else:
        dealer_cards = [str(card) for card in d.hand.cards]
        dealer_score = d.hand.score

    return {
        "player": {
            "name": p.name,
            "balance": p.balance,
            "bets": p.bets,
            "hands": player_hands,
            "active_hand_index": current_game_state["active_hand_index"]   
        },
        "dealer": {
            "cards": dealer_cards,
            "score": dealer_score
        },
        "round_active": round_active
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    player = player_service.login_player(username, password)
    if player:
        current_game_state["player"] = player
        state = {
            "username": player.name,
            "balance": player.balance
        }
        return jsonify({"status": "success", "message": "Login successful", "player": state})
    else:
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401
    
@app.route('/api/logout', methods=['POST'])
def logout():
    current_game_state["player"] = None
    current_game_state["dealer"] = None
    current_game_state["shoe"] = None
    current_game_state["round_active"] = False
    return jsonify({"status": "success", "message": "Logged out successfully"})

@app.route('/api/start_game', methods=['POST'])
def start_game():
    p = current_game_state["player"]
    if not p:
        return jsonify({"error": "Please login first"}), 401

    current_game_state["dealer"] = Dealer()
    current_game_state["shoe"] = Shoe(6)
    current_game_state["round_active"] = True

    d = current_game_state["dealer"]
    s = current_game_state["shoe"]

    p.place_bet(10)  
    p.receive_card(s.draw_card(), 0)
    d.receive_card(s.draw_card())
    p.receive_card(s.draw_card(), 0)
    d.receive_card(s.draw_card())

    bj_message = check_initial_blackjacks()
    state = get_game_json()

    if bj_message:
        state["result_message"] = bj_message
        player_service.save_player_state(p)

    return jsonify({"message": "Game started", "game_state": state})

@app.route('/api/hit', methods=['POST'])
def hit():
    if not current_game_state["round_active"]:
        return jsonify({"error": "No active round. Please start a new game."}), 400
    
    player = current_game_state["player"]
    shoe = current_game_state["shoe"]
    active_idx = current_game_state["active_hand_index"]
    hand = player.hands[active_idx]

    if not hand.is_busted:
        player.receive_card(shoe.draw_card(), active_idx)
        if hand.is_busted:
            return advance_turn()
        else:
            return jsonify({"message": "Hit successful", "game_state": get_game_json()})

@app.route('/api/stand', methods=['POST'])
def stand():
    if not current_game_state["round_active"]:
        return jsonify({"error" : "No active round"}), 400
    
    return advance_turn()

@app.route('/api/double_down', methods=['POST'])
def double_down():
    if not current_game_state["round_active"]:
        return jsonify({"error" : "No active round"}), 400
    
    p = current_game_state["player"]
    d = current_game_state["dealer"]
    s = current_game_state["shoe"]
    active_idx = current_game_state["active_hand_index"]

    if not p.can_double_down(active_idx):
        return jsonify({"error": "Cannot double down"}), 400
    
    p.double_down(active_idx)
    p.receive_card(s.draw_card(), active_idx)

    return advance_turn()

@app.route('/api/play_again', methods=['POST'])
def play_again():
    p = current_game_state["player"]
    d = current_game_state["dealer"]
    s = current_game_state["shoe"]

    if not p or not d or not s:
        return jsonify({"error": "Game not started"}), 400
    
    if p.balance < 10:
        return jsonify({"error": "Not enough balance to play again"}), 400
    
    p.clear_hand()
    d.clear_hand()
    
    if s.needs_reshuffle:
        s.build_and_shuffle()

    p.place_bet(10)
    p.receive_card(s.draw_card(), 0)
    d.receive_card(s.draw_card())
    p.receive_card(s.draw_card(), 0)
    d.receive_card(s.draw_card())

    current_game_state["round_active"] = True
    current_game_state["active_hand_index"] = 0

    bj_message = check_initial_blackjacks()
    state = get_game_json()

    if bj_message:
        state["result_message"] = bj_message

    return jsonify({"message": "New round started", "game_state": state})

@app.route('/api/split', methods=['POST'])
def split():
    if not current_game_state["round_active"]:
        return jsonify({"error": "No active round"}), 400
    
    p = current_game_state["player"]
    s = current_game_state["shoe"]
    active_idx = current_game_state["active_hand_index"]

    if not p.can_split(active_idx):
        return jsonify({"error": "Cannot split this hand"}), 400
    
    p.split_hand(active_idx)

    p.receive_card(s.draw_card(), active_idx)
    p.receive_card(s.draw_card(), len(p.hands) - 1)

    return jsonify({"message": "Hand split successfully", "game_state": get_game_json()})


def advance_turn():
    p = current_game_state["player"]
    d = current_game_state["dealer"]
    s = current_game_state["shoe"]

    if current_game_state["active_hand_index"] < len(p.hands) - 1:
        current_game_state["active_hand_index"] += 1
        return jsonify({"message": "Turn advanced to next hand", "game_state": get_game_json()})
    else:
        current_game_state["round_active"] = False

        all_busted = all(hand.is_busted for hand in p.hands)
        if not all_busted:
            while d.should_hit:
                d.receive_card(s.draw_card())
        return round_output(p, d, player_service)

def round_output(player, dealer, playerService):
    dealer_score = dealer.hand.score
    state = get_game_json()

    for i, hand in enumerate(player.hands):
        player_score = hand.score
        message = ""

        if hand.is_busted:
            player.lose_bet(i)
            message = "Hand busted! You lose!"
        elif dealer_score > 21:
            player.win_bet(i)
            message = "Dealer busted! You win!"
        elif player_score > dealer_score:
            player.win_bet(i)
            message = "You win!"
        elif player_score < dealer_score:
            player.lose_bet(i)
            message = "You lose!"
        else:
            player.push_bet(i)
            message = "It's a push!"

        state["player"]["hands"][i]["result_message"] = message

    playerService.save_player_state(player)
    state["result_message"] = "Round over"
    return jsonify({"message": "Round over", "game_state": state})
    
def check_initial_blackjacks():
    p = current_game_state["player"]
    d = current_game_state["dealer"]

    player_bj = p.hands[0].score == 21
    dealer_bj = d.hand.score == 21

    if player_bj and dealer_bj:
        current_game_state["round_active"] = False
        p.push_bet()
        return "Both player and dealer have Blackjack! It's a push!"
    elif player_bj:
        current_game_state["round_active"] = False
        p.win_bet(0, 1.5)
        return "Blackjack! You win!"
    return ""



if __name__ == '__main__':
    app.run(debug=True)