document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    const statusDiv = document.getElementById('status');
    const resetBtn = document.getElementById('resetBtn');
    let currentPlayer = 'X';
    let gameActive = true;
    const BOARD_SIZE = 15;
    const WIN_CONDITION = 5;
    let gameState = Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null));

    // Function to make an API call (Optional for AI)
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
        for (let row = 0; row < BOARD_SIZE; row++) {
            for (let col = 0; col < BOARD_SIZE; col++) {
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
        const row = parseInt(this.dataset.row, 10);
        const col = parseInt(this.dataset.col, 10);

        if (gameState[row][col] || this.textContent) return;

        this.textContent = currentPlayer;
        gameState[row][col] = currentPlayer;

        if (checkWin(row, col)) {
            statusDiv.textContent = `Hráč ${currentPlayer} Vyhrál!`;
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
            const aiCell = grid.querySelector(`.cell[data-row="${aiRow}"][data-col="${aiCol}"]`);
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
                statusDiv.textContent = `Na řadě je hráč: ${currentPlayer}`;
            }
        }
        */
    }

    // Check for a win condition
    function checkWin(row, col) {
        const player = gameState[row][col];
        if (!player) return false;

        const directions = [
            { dr: 0, dc: 1 },
            { dr: 1, dc: 0 },
            { dr: 1, dc: 1 },
            { dr: 1, dc: -1 }
        ];

        for (const { dr, dc } of directions) {
            let count = 1;
            let winningCells = [[row, col]];

            let r = row + dr;
            let c = col + dc;
            while (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE && gameState[r][c] === player) {
                count++;
                winningCells.push([r, c]);
                r += dr;
                c += dc;
            }

            r = row - dr;
            c = col - dc;
            while (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE && gameState[r][c] === player) {
                count++;
                winningCells.push([r, c]);
                r -= dr;
                c -= dc;
            }

            if (count >= WIN_CONDITION) {
                window.winningCells = winningCells;
                return true;
            }
        }

        return false;
    }

    function highlightWinningCells() {
        if (!window.winningCells) return;
        window.winningCells.forEach(([row, col]) => {
            const cell = grid.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
            if (cell) {
                cell.classList.add('winning-cell');
            }
        });
    }

    function isDraw() {
        for (let row = 0; row < BOARD_SIZE; row++) {
            for (let col = 0; col < BOARD_SIZE; col++) {
                if (!gameState[row][col]) {
                    return false;
                }
            }
        }
        return true;
    }

    function resetGame() {
        currentPlayer = 'X';
        gameActive = true;
        statusDiv.textContent = `Na řadě je hráč: ${currentPlayer}`;
        gameState = Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null));
        const cells = grid.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.textContent = '';
            cell.classList.remove('winning-cell');
        });
        delete window.winningCells;
    }

    resetBtn.addEventListener('click', resetGame);

    initializeGrid();
});