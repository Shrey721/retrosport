const API_URL = "/api";

const playersList = document.getElementById("players-list");
const playerDetails = document.getElementById("player-details");
const aiAssistant = document.getElementById("ai-assistant");
const chatBox = document.getElementById("chat-box");
const aiForm = document.getElementById("ai-form");
const aiQuestionInput = document.getElementById("ai-question");

let currentPlayer = null;

async function fetchPlayers() {
    const res = await fetch(`${API_URL}/players`);
    const players = await res.json();
    playersList.innerHTML = '<h2>Players</h2>' + players.map(player => `
        <div class="player-item" data-id="${player.id}">
            <strong>${player.name}</strong> (${player.position})
        </div>
    `).join('');
    document.querySelectorAll('.player-item').forEach(item => {
        item.onclick = () => showPlayerDetails(item.dataset.id);
    });
}

async function showPlayerDetails(playerId) {
    const res = await fetch(`${API_URL}/players/${playerId}`);
    const player = await res.json();
    currentPlayer = player;
    playerDetails.style.display = '';
    aiAssistant.style.display = '';
    playerDetails.innerHTML = `
        <h2>${player.name} <span style="font-size:0.7em;color:#888;">(${player.position})</span></h2>
        <ul>
            <li>Games: ${player.stats.games}</li>
            <li>Goals: ${player.stats.goals}</li>
            <li>Assists: ${player.stats.assists}</li>
            <li>Minutes: ${player.stats.minutes}</li>
        </ul>
    `;
    chatBox.innerHTML = '';
}

aiForm.onsubmit = async (e) => {
    e.preventDefault();
    if (!currentPlayer) return;
    const question = aiQuestionInput.value;
    chatBox.innerHTML += `<div class="ai-question"><strong>You:</strong> ${question}</div>`;
    aiQuestionInput.value = '';
    const res = await fetch(`${API_URL}/players/${currentPlayer.id}/ai`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
    });
    const data = await res.json();
    chatBox.innerHTML += `<div class="ai-answer"><strong>AI:</strong> ${data.answer}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
};

fetchPlayers();
