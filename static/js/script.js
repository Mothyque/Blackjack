let lastKnownState = null;
let displayHandIndex = 0;
async function login(){
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    const errorMsg = document.getElementById('loginErrorMessage');
    const loginScreen = document.getElementById('loginScreen');
    const gameBoard = document.getElementById('gameBoard');

    try
    {
        const response = await fetch('/api/login',{
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: user, password: pass })
        });

        const data = await response.json();
        if (response.ok)
        {
            loginScreen.style.display = 'none';
            gameBoard.style.display = 'block';
            startGame();
        }
        else
        {
            errorMsg.innerText = data.message;
            errorMsg.style.display = 'block';
            document.getElementById('username').value = user;
            document.getElementById('password').value = '';
        }
    }
    catch (error)
    {
        console.error('Error logging in:', error);
    }
}

async function startGame() {
    const response = await fetch('/api/start_game', {method: 'POST'});
    const data = await response.json();
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

    lastKnownState = state;
    if (state.round_active) {
        displayHandIndex = state.player.active_hand_index;
    }

    if (displayHandIndex >= state.player.hands.length) {
        displayHandIndex = 0;
    }

    const playerHand = state.player.hands[displayHandIndex];

    document.getElementById('playerNameDisplay').innerText = state.player.name + ` (Balance: $${state.player.balance})`;

    drawCards('playerCards', playerHand.cards);
    document.getElementById('playerScore').innerText = 'Score: ' + playerHand.score;

    drawCards('dealerCards', state.dealer.cards);
    document.getElementById('dealerScoreDisplay').innerText = 'Score: ' + state.dealer.score;

    const btnHit = document.getElementById('btnHit');
    const btnStand = document.getElementById('btnStand');
    const btnDouble = document.getElementById('btnDouble');
    const btnSplit = document.getElementById('btnSplit');
    const btnPrevHand = document.getElementById('btnPrevHand');
    const btnNextHand = document.getElementById('btnNextHand');
    const btnPlayAgain = document.getElementById('btnPlayAgain');
    const btnLogin = document.getElementById('btnLogin');
    const gameMessage = document.getElementById('gameMessage');
    const handIndicator = document.getElementById('handIndicatorDisplay');

    if (state.player.hands.length > 1) {
        handIndicator.innerText = `Hand ${displayHandIndex + 1} of ${state.player.hands.length}`;
        handIndicator.style.display = 'block';
    } else {
        handIndicator.style.display = 'none';
    }

    if (state.round_active && !playerHand.is_busted)
    {
        btnPrevHand.style.display = 'none';
        btnNextHand.style.display = 'none';
        btnPlayAgain.style.display = 'none';
        gameMessage.innerText = '';

        if (playerHand.score == 21)
        {
            btnHit.style.display = 'none';
            btnStand.style.display = 'none';
            btnDouble.style.display = 'none';
            btnSplit.style.display = 'none';
            stand();
        }
        else
        {
            btnHit.style.display = 'inline-block';
            btnStand.style.display = 'inline-block';
            btnDouble.style.display = playerHand.can_double ? 'inline-block' : 'none';
            btnSplit.style.display = playerHand.can_split ? 'inline-block' : 'none';
        }
    }
    else
    {
        btnHit.style.display = 'none';
        btnStand.style.display = 'none';
        btnLogin.style.display = 'none';
        btnDouble.style.display = 'none';
        btnSplit.style.display = 'none';
        
        if (!state.round_active) {
            btnPlayAgain.style.display = 'inline-block';
            btnPrevHand.style.display = displayHandIndex > 0 ? 'inline-block' : 'none';
            btnNextHand.style.display = displayHandIndex < state.player.hands.length - 1 ? 'inline-block' : 'none';
            
            const finalMessage = playerHand.result_message ? playerHand.result_message : state.result_message;
            gameMessage.innerText = finalMessage;

            const msglower = finalMessage.toLowerCase();
            if (msglower.includes('win')) {
                gameMessage.style.color = "#006400";
            } else if (msglower.includes('lose') || msglower.includes('busted')) {
                gameMessage.style.color = "#ff0000";
            } else {
                gameMessage.style.color = "#f1c40f";
            }
        }
        gameMessage.style.display = 'block';
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

async function logout() {
    try {
        await fetch('/api/logout', { method: 'POST' });

        document.getElementById('gameBoard').style.display = 'none';
        document.getElementById('loginScreen').style.display = 'block';
        document.getElementById('btnLogin').style.display = 'inline-block';

        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
        document.getElementById('loginErrorMessage').style.display = 'none';
        
        document.getElementById('gameMessage').innerText = '';
        document.getElementById('playerCards').innerHTML = '';
        document.getElementById('dealerCards').innerHTML = '';
        document.getElementById('playerScore').innerText = 'Score: 0';
        document.getElementById('dealerScoreDisplay').innerText = 'Score: ?';
    }
    catch (error) {
        console.error('Error logging out:', error);
    }
}

async function doubleDown() {
    const response = await fetch('/api/double_down', { method: 'POST' });
    const data = await response.json();
    if (response.ok) {
        updateUI(data.game_state);
    } else {
        alert(data.error)
    }
}

async function splitHand() {
    const response = await fetch('/api/split', { method: 'POST' });
    const data = await response.json();
    if (response.ok) {
        updateUI(data.game_state);
    } else {
        alert(data.error);
    }
}

function prevHand() {
    if (displayHandIndex > 0) {
        displayHandIndex--;
        updateUI(lastKnownState);
    }
}

function nextHand() {
    if (lastKnownState && displayHandIndex < lastKnownState.player.hands.length - 1) {
        displayHandIndex++;
        updateUI(lastKnownState);
    }
}

function exitApp() {
    if (confirm("Are you sure you want to exit the game?")) {
        window.close();
    }
}
        