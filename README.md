# FreeCell Solver

A modern web-based FreeCell solitaire game with an AI solver built using Python FastAPI and vanilla JavaScript. The game features a clean, responsive interface and includes a Monte Carlo Tree Search (MCTS) algorithm that can automatically play moves.

## Features

- **Interactive Web Interface**: Clean, modern UI with click-to-move functionality
- **AI Solver**: Monte Carlo Tree Search algorithm that can suggest and play optimal moves
- **Game Controls**: New game, undo moves, computer play, and quit options
- **Responsive Design**: Works on desktop and mobile devices
- **Visual Feedback**: Card selection highlighting and move validation
- **Game State Management**: Full undo/redo functionality with move history

## Screenshots

The game features:
- **Free Cells**: 4 temporary storage slots for cards
- **Home Cells**: 4 foundation piles (one for each suit)
- **Table Columns**: 8 columns where the main gameplay occurs
- **Action Buttons**: Easy access to all game functions

## Installation

### Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for running the server)

### Setup

1. **Clone or download the project files**
   ```bash
   # Ensure you have all these files in your project directory:
   # - app.py
   # - main.py
   # - index.html
   # - styles.css
   # - script.js
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Run the server**
   ```bash
   uvicorn app:app --reload
   ```

4. **Open your browser**
   Navigate to `http://localhost:8000` to start playing!

## How to Play

### Basic Rules
FreeCell is a solitaire card game where the goal is to move all cards to the home cells (foundations) in ascending order by suit.

### Game Layout
- **Free Cells (4)**: Temporary storage for individual cards
- **Home Cells (4)**: Foundation piles for each suit (Clubs, Diamonds, Hearts, Spades)
- **Table Columns (8)**: Main playing area with cascading cards

### Valid Moves
1. **Column to Column**: Cards must be placed in descending order with alternating colors
2. **Column to Free Cell**: Any exposed card can be moved to an empty free cell
3. **Free Cell to Column**: Cards from free cells can be moved to valid column positions
4. **Column/Free Cell to Home**: Cards can be moved to home cells in ascending order by suit (A, 2, 3... K)

### Controls
- **Click to Select**: Click on a card to select it (highlighted in blue)
- **Click to Move**: Click on a destination to move the selected card
- **New Game**: Start a fresh game with shuffled cards
- **Computer Play**: Let the AI make a move using MCTS algorithm
- **Undo**: Reverse the last move
- **Quit**: End the current game

## Technical Details

### Architecture
- **Backend**: Python FastAPI server handling game logic and AI
- **Frontend**: Vanilla JavaScript with modern CSS styling
- **AI Algorithm**: Monte Carlo Tree Search (MCTS) for move optimization

### API Endpoints
- `GET /` - Serve the main game interface
- `GET /get_game_state` - Get current board state
- `POST /start` - Start a new game
- `POST /move_column` - Move card between columns
- `POST /move_to_free` - Move card to free cell
- `POST /move_from_free` - Move card from free cell
- `POST /column_to_home` - Move card to home cell
- `POST /free_to_home` - Move card from free cell to home
- `GET /computer_play` - Get AI move suggestion
- `POST /undo` - Undo last move
- `GET /is_game_won` - Check win condition

### File Structure
```
freecell-solver/
├── app.py          # FastAPI server and API endpoints
├── main.py         # Game logic and MCTS algorithm
├── index.html      # Main HTML interface
├── styles.css      # Custom CSS styling
├── script.js       # Frontend JavaScript logic
└── README.md       # This file
```

## AI Algorithm

The computer player uses **Monte Carlo Tree Search (MCTS)** to determine optimal moves:

1. **Selection**: Navigate down the game tree using UCB1 formula
2. **Expansion**: Add new possible moves to the tree
3. **Simulation**: Play out random games to completion
4. **Backpropagation**: Update node statistics based on simulation results

The AI prioritizes moves to home cells and uses 100 simulations by default for move selection.

## Customization

### Adjusting AI Difficulty
Modify the simulation count in `script.js`:
```javascript
const response = await fetch('/computer_play?sim=100'); // Change 100 to desired number
```

### Styling
Edit `styles.css` to customize:
- Card appearance and sizing
- Color schemes
- Hover effects and animations
- Layout and spacing

### Game Rules
Modify `main.py` to adjust:
- Move validation logic
- Scoring system
- Win conditions
- Card shuffling algorithm

## Troubleshooting

### Common Issues

1. **Server won't start**
   - Ensure FastAPI and Uvicorn are installed: `pip install fastapi uvicorn`
   - Check that port 8000 is available

2. **Cards not displaying**
   - Verify all files are in the same directory
   - Check browser console for JavaScript errors
   - Ensure server is running on `http://localhost:8000`

3. **AI not working**
   - Computer play requires valid moves to be available
   - Check console for API errors
   - Verify game state is properly initialized

### Performance Tips
- Reduce MCTS simulations for faster AI moves
- Use browser dev tools to monitor API calls
- Clear browser cache if experiencing display issues

## Contributing

Feel free to contribute improvements:
- Enhanced AI algorithms
- Better move validation
- Additional game statistics
- UI/UX improvements
- Mobile responsiveness enhancements

## License

This project is open source and available under the MIT License.

## Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Inter Font](https://fonts.google.com/specimen/Inter) - Clean, readable typography

---

Enjoy playing FreeCell! 🃏
