async function startGame() {
    const name = document.getElementById('playerName').value;
    const response = await fetch('/api/start_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({name : name })
    });
    const data = await response.json();
    document.getElementById('setupArea').style.display = 'none';
    document.getElementById('gameBoard').style.display = 'block';
    
    updateUI(data.game_state);
}

async function hit(){
    const response = await fetch('/api/hit', { method: 'POST' });
    const data = await response.json();
    updateUI(data.game_state);
}

async function stand(){
    const response = await fetch('/api/stand', { method: 'POST' });
    const data = await response.json();
    updateUI(data.game_state);
}

async function playAgain() {
    const response = await fetch('/api/play_again', { method: 'POST' });
    const data = await response.json();
    updateUI(data.game_state);
}

function updateUI(state) {
    document.getElementById('playerNameDisplay').innerText = state.player.name + ` (Balance: $${state.player.balance})`;

    const playerHand = state.player.hands[0];
    drawCards('playerCards', playerHand.cards);
    document.getElementById('playerScore').innerText = 'Score: ' + playerHand.score;

    drawCards('dealerCards', state.dealer.cards);
    document.getElementById('dealerScoreDisplay').innerText = 'Score: ' + state.dealer.score;

    const btnHit = document.getElementById('btnHit');
    const btnStand = document.getElementById('btnStand');
    const btnPlayAgain = document.getElementById('btnPlayAgain');
    const gameMessage = document.getElementById('gameMessage');

    if (state.round_active && !playerHand.is_busted)
    {
        btnHit.style.display = 'inline-block';
        btnStand.style.display = 'inline-block';
        btnPlayAgain.style.display = 'none';
        gameMessage.innerText = '';
    }
    else
    {
        btnHit.style.display = 'none';
        btnStand.style.display = 'none';
        btnPlayAgain.style.display = 'inline-block';
        if (state.result_message) {
            gameMessage.innerText = state.result_message;
        }
        else {
            gameMessage.innerText = "Bust! You lose.";
        }
    }
}

function drawCards(containerId, cardsArray) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    cardsArray.forEach(card => {
        const cardElement = document.createElement('div');
        cardElement.className = 'card';
        if (card == "🂠"){
            cardElement.classList.add('hidden-card');
        }
        if(card.includes('♥') || card.includes('♦')) {
            cardElement.classList.add('red');
        }
        cardElement.innerText = card;
        container.appendChild(cardElement);
    });
}