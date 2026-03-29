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
    document.getElementById('playerNameDisplay').innerText = state.player.name + ` (Balance: $${state.player.balance})`;

    const playerHand = state.player.hands[0];
    drawCards('playerCards', playerHand.cards);
    document.getElementById('playerScore').innerText = 'Score: ' + playerHand.score;

    drawCards('dealerCards', state.dealer.cards);
    document.getElementById('dealerScoreDisplay').innerText = 'Score: ' + state.dealer.score;

    const btnHit = document.getElementById('btnHit');
    const btnStand = document.getElementById('btnStand');
    const btnPlayAgain = document.getElementById('btnPlayAgain');
    const btnLogin = document.getElementById('btnLogin');
    const gameMessage = document.getElementById('gameMessage');

    if (state.round_active && !playerHand.is_busted)
    {
        if (playerHand.score == 21)
        {
            btnHit.style.display = 'none';
            btnStand.style.display = 'none';
            stand();
        }
        else
        {
            btnHit.style.display = 'inline-block';
        }
        btnStand.style.display = 'inline-block';
        btnPlayAgain.style.display = 'none';
        btnLogin.style.display = 'none';
        gameMessage.innerText = '';
    }
    else
    {
        btnHit.style.display = 'none';
        btnStand.style.display = 'none';
        btnLogin.style.display = 'none';
        btnPlayAgain.style.display = 'inline-block';
        if (state.result_message) {
            gameMessage.innerText = state.result_message;
            gameMessage.style.display = 'block';
        }
        else {
            gameMessage.innerText = "Bust! You lose.";
            gameMessage.style.display = 'block';
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