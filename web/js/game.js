// game.js

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    const statusDiv = document.getElementById('status');
    const resetBtn = document.getElementById('resetBtn');
    let currentPlayer = 'X';
    let gameActive = true;
    const gameState = Array(15).fill(null).map(() => Array(15).fill(null));

    // Function to make an API call
    async function callAPI(endpoint, data) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    }

    // Initialize the grid
    function initializeGrid() {
        grid.innerHTML = '';
        for (let row = 0; row < 15; row++) {
            for (let col = 0; col < 15; col++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = row;
                cell.dataset.col = col;

                cell.addEventListener('click', handleCellClick);

                grid.appendChild(cell);
            }
        }
    }

    // Handle cell click
    async function handleCellClick() {
        if (!gameActive) return;
        const row = this.dataset.row;
        const col = this.dataset.col;

        if (gameState[row][col] || this.textContent) return;

        this.textContent = currentPlayer;
        gameState[row][col] = currentPlayer;

        if (checkWin(row, col)) {
            statusDiv.textContent = `Hráč ${currentPlayer} vyhrál!`;
            gameActive = false;
            highlightWinningCells();
            return;
        }

        if (isDraw()) {
            statusDiv.textContent = `Remíza!`;
            gameActive = false;
            return;
        }

        // Switch player
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        statusDiv.textContent = `Na řadě je hráč: ${currentPlayer}`;

        // Optional: Call API for AI move
        /*
        const response = await callAPI('/api/move', {
            player: currentPlayer,
            row,
            col,
            gameState
        });

        if (response && response.aiMove) {
            const { row: aiRow, col: aiCol } = response.aiMove;
            const aiCell = grid.children[aiRow * 15 + aiCol];
            if (aiCell && !aiCell.textContent) {
                aiCell.textContent = 'O';
                gameState[aiRow][aiCol] = 'O';

                if (checkWin(aiRow, aiCol)) {
                    statusDiv.textContent = `Player O Wins!`;
                    gameActive = false;
                    highlightWinningCells();
                    return;
                }

                if (isDraw()) {
                    statusDiv.textContent = `It's a Draw!`;
                    gameActive = false;
                    return;
                }

                currentPlayer = 'X';
                statusDiv.textContent = `Current Player: ${currentPlayer}`;
            }
        }
        */
    }

    // Check for a win condition
    function checkWin(row, col) {
        const directions = [
            { dr: -1, dc: 0 }, // Up
            { dr: 1, dc: 0 },  // Down
            { dr: 0, dc: -1 }, // Left
            { dr: 0, dc: 1 },  // Right
            { dr: -1, dc: -1 },// Up-Left
            { dr: -1, dc: 1 }, // Up-Right
            { dr: 1, dc: -1 }, // Down-Left
            { dr: 1, dc: 1 }   // Down-Right
        ];
        const player = gameState[row][col];
        let count = 1;
        let winningCells = [[parseInt(row), parseInt(col)]];

        directions.forEach(dir => {
            let r = parseInt(row) + dir.dr;
            let c = parseInt(col) + dir.dc;
            while (r >= 0 && r < 15 && c >= 0 && c < 15 && gameState[r][c] === player) {
                count++;
                winningCells.push([r, c]);
                r += dir.dr;
                c += dir.dc;
            }
        });

        if (count >= 5) {
            window.winningCells = winningCells; // Store for highlighting
            return true;
        }
        return false;
    }

    // Highlight winning cells
    function highlightWinningCells() {
        if (!window.winningCells) return;
        window.winningCells.forEach(([row, col]) => {
            const index = row * 15 + col;
            const cell = grid.children[index];
            if (cell) {
                cell.style.backgroundColor = '#27ae60';
                cell.style.color = '#fff';
                cell.classList.add('disabled');
            }
        });
    }

    // Check for a draw
    function isDraw() {
        return gameState.every(row => row.every(cell => cell));
    }

    // Reset the game
    resetBtn.addEventListener('click', () => {
        currentPlayer = 'X';
        gameActive = true;
        statusDiv.textContent = `Na řadě je hráč: ${currentPlayer}`;
        for (let row = 0; row < 15; row++) {
            for (let col = 0; col < 15; col++) {
                gameState[row][col] = null;
            }
        }
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.textContent = '';
            cell.style.backgroundColor = '#ecf0f1';
            cell.style.color = '#2c3e50';
            cell.classList.remove('disabled');
        });
        delete window.winningCells;
    });

    // Initialize the game on page load
    initializeGrid();
});