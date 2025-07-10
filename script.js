document.addEventListener('DOMContentLoaded', () => {
    const gameStatus = document.getElementById('game-status');
    const freeCellsDiv = document.getElementById('free-cells');
    const homeCellsDiv = document.getElementById('home-cells');
    const tableColumnsDiv = document.getElementById('table-columns');

    // Action Buttons
    const newGameBtn = document.getElementById('new-game-btn');
    const computerPlayBtn = document.getElementById('computer-play-btn');
    const undoBtn = document.getElementById('undo-btn');
    const quitBtn = document.getElementById('quit-btn');

    // Global state for click-to-move
    let selectedSource = null; // { type: 'column' | 'free', index: number, card: string }
    let selectedCardElement = null; // The DOM element of the selected card

    // Helper to display messages
    function displayMessage(message, isError = false) {
        gameStatus.textContent = message;
        gameStatus.className = `text-center text-lg font-semibold mb-4 ${isError ? 'text-red-600' : 'text-green-600'}`;
    }

    // Function to get rank and suit symbol from card string (e.g., "Ac" -> "A", "♣")
    function getCardDetails(cardString) {
        const rank = cardString[0];
        const suitChar = cardString[1];
        let suitSymbol = '';
        let suitColorClass = '';

        switch (suitChar) {
            case 'c': suitSymbol = '♣'; suitColorClass = 'suit-black'; break;
            case 'd': suitSymbol = '♦'; suitColorClass = 'suit-red'; break;
            case 'h': suitSymbol = '♥'; suitColorClass = 'suit-red'; break;
            case 's': suitSymbol = '♠'; suitColorClass = 'suit-black'; break;
            default: suitSymbol = ''; suitColorClass = ''; // For "0c" initializers
        }
        return { rank, suitSymbol, suitColorClass };
    }

    // Function to deselect any currently selected card
    function deselectCard() {
        if (selectedCardElement) {
            selectedCardElement.classList.remove('selected-card');
            selectedCardElement = null;
        }
        selectedSource = null;
        displayMessage('Click a card to start a move.');
    }

    // Handle clicks on cards (source selection or destination)
    function handleCardClick(event) {
        const clickedCardElement = event.currentTarget; // The card div itself
        const cardValue = clickedCardElement.dataset.card;
        const clickedSourceType = clickedCardElement.dataset.sourceType; // Type of the clicked card's location
        const clickedSourceIndex = parseInt(clickedCardElement.dataset.sourceIndex);

        // If the same card is clicked again, deselect it
        if (selectedCardElement === clickedCardElement) {
            deselectCard();
            return;
        }

        // If a card is already selected, this click is a potential destination
        if (selectedSource !== null) {
            let destType;
            let destIndex;

            if (clickedSourceType === 'column') {
                // If clicking on a card in a column, the destination is that column
                destType = 'column';
                destIndex = clickedSourceIndex;
            } else if (clickedSourceType === 'home') {
                // If clicking on a card in a home cell, the destination is that home cell
                destType = 'home';
                destIndex = clickedSourceIndex;
            } else {
                // Clicking on a card in a free cell should not be a destination for another card
                displayMessage('Cannot move a card to another FreeCell card.', true);
                deselectCard();
                return;
            }

            attemptMove(selectedSource, { type: destType, index: destIndex });
            // deselectCard() will be called after attemptMove completes and renderGameState is called
        } else {
            // No card selected yet, this is the first click (source selection)
            // Only allow selecting the bottom-most card in a column
            if (clickedSourceType === 'column' && clickedCardElement.nextElementSibling) {
                displayMessage('You can only select the bottom-most card in a column.', true);
                return;
            }
            // Home cells are not valid sources in FreeCell
            if (clickedSourceType === 'home') {
                displayMessage('Cards cannot be moved out of Home Cells.', true);
                return;
            }


            selectedSource = { type: clickedSourceType, index: clickedSourceIndex, card: cardValue };
            selectedCardElement = clickedCardElement;
            selectedCardElement.classList.add('selected-card'); // Add visual highlight
            displayMessage(`Selected ${cardValue} from ${clickedSourceType} ${clickedSourceIndex}. Now click a destination.`);
        }
    }

    // Handle clicks on empty slots (destination selection)
    function handleEmptySlotClick(event) {
        if (selectedSource === null) {
            return; // No card selected yet
        }

        const clickedElement = event.currentTarget;
        const destType = clickedElement.dataset.destinationType; // 'column' or 'home' or 'free'
        const destIndex = parseInt(clickedElement.dataset.destinationIndex);

        attemptMove(selectedSource, { type: destType, index: destIndex });
        // deselectCard() will be called after attemptMove completes and renderGameState is called
    }

    // Function to perform the move via API
    async function attemptMove(source, destination) {
        let success = false;
        let message = 'Invalid move combination.';
        let endpoint = '';
        let params = new URLSearchParams();

        if (source.type === 'column' && destination.type === 'column') {
            endpoint = '/move_column';
            params.append('src', source.index);
            params.append('dst', destination.index);
        } else if (source.type === 'column' && destination.type === 'free') {
            endpoint = '/move_to_free';
            params.append('src', source.index);
        } else if (source.type === 'free' && destination.type === 'column') {
            endpoint = '/move_from_free';
            params.append('src', source.index);
            params.append('dst', destination.index);
        } else if (source.type === 'column' && destination.type === 'home') {
            endpoint = '/column_to_home';
            params.append('src', source.index);
        } else if (source.type === 'free' && destination.type === 'home') {
            endpoint = '/free_to_home';
            params.append('src', source.index);
        } else {
            displayMessage(message, true);
            await renderGameState(); // Re-render to clear selection
            return;
        }

        try {
            const response = await fetch(`${endpoint}?${params.toString()}`, { method: 'POST' });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            success = await response.json();
            message = success ? 'Move successful!' : 'Invalid move. Please try again.';
        } catch (error) {
            console.error('Error performing move:', error);
            message = `Failed to perform move: ${error.message}`;
            success = false;
        }

        displayMessage(message, !success);
        await renderGameState(); // Re-render to update board and clear selection
    }


    // Function to render the game state
    async function renderGameState() {
        try {
            const response = await fetch('/get_game_state');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const gameState = await response.json();

            // Clear previous content and re-add empty slots for click targets
            freeCellsDiv.innerHTML = '';
            for (let i = 0; i < 4; i++) {
                const emptySlot = document.createElement('div');
                emptySlot.className = 'empty-slot';
                emptySlot.dataset.destinationType = 'free';
                emptySlot.dataset.destinationIndex = i;
                emptySlot.addEventListener('click', handleEmptySlotClick);
                freeCellsDiv.appendChild(emptySlot);
            }

            homeCellsDiv.innerHTML = '';
            for (let i = 0; i < 4; i++) {
                const emptySlot = document.createElement('div');
                emptySlot.className = 'empty-slot';
                emptySlot.dataset.destinationType = 'home';
                emptySlot.dataset.destinationIndex = i;
                emptySlot.addEventListener('click', handleEmptySlotClick);
                homeCellsDiv.appendChild(emptySlot);
            }

            tableColumnsDiv.innerHTML = '';


            // Render Free Cells
            if (gameState.free && gameState.free.length > 0) {
                gameState.free.forEach((card, index) => {
                    const cardDetails = getCardDetails(card);
                    const cardDiv = document.createElement('div');
                    cardDiv.className = `card ${cardDetails.suitColorClass}`;
                    cardDiv.dataset.card = card;
                    cardDiv.dataset.sourceType = 'free';
                    cardDiv.dataset.sourceIndex = index; // Index within the free cells array
                    cardDiv.innerHTML = `<span class="card-rank">${cardDetails.rank}</span><span class="card-suit">${cardDetails.suitSymbol}</span>`;
                    cardDiv.addEventListener('click', handleCardClick);
                    // Replace the empty slot at this index with the card
                    if (freeCellsDiv.children[index]) {
                        freeCellsDiv.children[index].replaceWith(cardDiv);
                    } else {
                        freeCellsDiv.appendChild(cardDiv); // Fallback if somehow slot not there
                    }
                });
            }

            // Render Home Cells
            if (gameState.home && gameState.home.length > 0) {
                gameState.home.forEach((homeStack, index) => {
                    if (homeStack.length > 1) { // If there's a card on top of "0"
                        const card = homeStack[homeStack.length - 1];
                        const cardDetails = getCardDetails(card);
                        const cardDiv = document.createElement('div');
                        cardDiv.className = `card ${cardDetails.suitColorClass}`;
                        cardDiv.dataset.card = card;
                        // Home cells are typically not sources in FreeCell, so no sourceType/sourceIndex needed
                        // BUT they can be destinations for a successor card
                        cardDiv.dataset.destinationType = 'home'; // Add destination type
                        cardDiv.dataset.destinationIndex = index; // Add destination index
                        cardDiv.dataset.sourceType = 'home'; // Add source type for click handling
                        cardDiv.dataset.sourceIndex = index; // Add source index for click handling
                        cardDiv.innerHTML = `<span class="card-rank">${cardDetails.rank}</span><span class="card-suit">${cardDetails.suitSymbol}</span>`;
                        cardDiv.addEventListener('click', handleCardClick); // Add click listener
                        // Replace the empty slot at this index with the card
                        if (homeCellsDiv.children[index]) {
                            homeCellsDiv.children[index].replaceWith(cardDiv);
                        } else {
                            homeCellsDiv.appendChild(cardDiv); // Fallback
                        }
                    }
                });
            }

            // Render Table Columns
            if (gameState.table && gameState.table.length > 0) {
                gameState.table.forEach((column, colIndex) => {
                    const columnDiv = document.createElement('div');
                    columnDiv.className = 'column';

                    const colHeader = document.createElement('h3');
                    colHeader.className = 'column-header';
                    colHeader.textContent = `Col ${colIndex}`;
                    columnDiv.appendChild(colHeader);

                    if (column.length > 0) {
                        // If column has cards, only cards are clickable for source/destination
                        column.forEach((card, cardPos) => {
                            const cardDetails = getCardDetails(card);
                            const cardDiv = document.createElement('div');
                            cardDiv.className = `card ${cardDetails.suitColorClass}`;
                            cardDiv.dataset.card = card;
                            cardDiv.dataset.sourceType = 'column';
                            cardDiv.dataset.sourceIndex = colIndex;
                            cardDiv.dataset.cardPosition = cardPos; // Position within the column
                            cardDiv.innerHTML = `<span class="card-rank">${cardDetails.rank}</span><span class="card-suit">${cardDetails.suitSymbol}</span>`;
                            cardDiv.addEventListener('click', handleCardClick);
                            columnDiv.appendChild(cardDiv);
                        });
                    } else {
                        // If column is empty, the columnDiv itself is the click target for destination
                        columnDiv.classList.add('empty-column');
                        columnDiv.dataset.destinationType = 'column';
                        columnDiv.dataset.destinationIndex = colIndex;
                        columnDiv.addEventListener('click', handleEmptySlotClick);

                        const emptySlot = document.createElement('div');
                        emptySlot.className = 'text-center text-gray-400 text-sm mt-4';
                        emptySlot.textContent = 'Empty';
                        columnDiv.appendChild(emptySlot);
                    }
                    tableColumnsDiv.appendChild(columnDiv);
                });
            } else {
                tableColumnsDiv.textContent = 'No columns to display.';
                tableColumnsDiv.classList.add('text-gray-500', 'text-center');
            }

            // Check if game is won
            const isGameWonResponse = await fetch('/is_game_won');
            const isWon = await isGameWonResponse.json();
            if (isWon) {
                displayMessage('Congratulations! You won the game!', false);
            }

            // After rendering, deselect any card
            deselectCard();

        } catch (error) {
            console.error('Error rendering game state:', error);
            displayMessage('Failed to load game state. Please try starting a new game.', true);
        }
    }

    // Event Listeners for Actions
    newGameBtn.addEventListener('click', async () => {
        try {
            await fetch('/start', { method: 'POST' });
            displayMessage('New game started!');
            await renderGameState();
        } catch (error) {
            console.error('Error starting new game:', error);
            displayMessage('Failed to start new game.', true);
        }
    });

    computerPlayBtn.addEventListener('click', async () => {
        displayMessage('Computer is thinking...', false);
        try {
            const response = await fetch('/computer_play?sim=100'); // Pass simulations count
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const bestMove = await response.json();

            if (bestMove) {
                displayMessage(`Computer made move: ${JSON.stringify(bestMove)}`);
            } else {
                displayMessage('Computer could not find a valid move or game is stuck.', true);
            }
            await renderGameState();
        } catch (error) {
            console.error('Error during computer play:', error);
            displayMessage('Failed for computer to make a move.', true);
        }
    });

    undoBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/undo', { method: 'POST' });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const success = await response.json();
            if (success) {
                displayMessage('Undo successful!');
            } else {
                displayMessage('Cannot undo further.', true);
            }
            await renderGameState();
        } catch (error) {
            console.error('Error during undo:', error);
            displayMessage('Failed to undo move.', true);
        }
    });

    quitBtn.addEventListener('click', () => {
        displayMessage('Game quit. Goodbye!', false);
        // Optionally, reset UI or disable controls
        freeCellsDiv.innerHTML = '';
        homeCellsDiv.innerHTML = '';
        tableColumnsDiv.innerHTML = '';
        freeCellsDiv.textContent = 'Empty';
        homeCellsDiv.textContent = 'Empty';
        tableColumnsDiv.textContent = 'Game not started.';
        deselectCard(); // Clear any selection
    });

    // Initial render when the page loads
    renderGameState();
});
