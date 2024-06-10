import React, { useState } from 'react';
import './ShogiBoard.css';
import Piece from './Piece';

const ShogiBoard: React.FC = () => {
    const rows = 9;
    const cols = 9;

    // Initial positions of the pieces
    const initialBoard = [
        ["l", "n", "s", "g", "k", "g", "s", "n", "l"],
        [null, "r", null, null, null, null, null, "b", null],
        ["p", "p", "p", "p", "p", "p", "p", "p", "p"],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        [null, null, null, null, null, null, null, null, null],
        ["P", "P", "P", "P", "P", "P", "P", "P", "P"],
        [null, "B", null, null, null, null, null, "R", null],
        ["L", "N", "S", "G", "K", "G", "S", "N", "L"]
    ];

    const [move, setMove] = useState('');

    const pieceSymbols: { [key: string]: string } = {
        'p': '歩', 'l': '香', 'n': '桂', 's': '銀', 'g': '金', 'k': '王', 'r': '飛', 'b': '角',
        'P': '歩', 'L': '香', 'N': '桂', 'S': '銀', 'G': '金', 'K': '玉', 'R': '飛', 'B': '角'
    };

    const handleMoveSubmit = () => {
        setMove('');
    };

    const renderBoard = () => {
        let board = [];
        for (let row = 0; row < rows; row++) {
            let cells = [];
            for (let col = 0; col < cols; col++) {
                const piece = initialBoard[row][col];
                cells.push(
                    <div key={`${row}-${col}`} className="cell">
                        {piece && <Piece symbol={pieceSymbols[piece]} isBlack={piece === piece.toLowerCase()} />}
                    </div>
                );
            }
            board.push(
                <div key={row} className="row">
                    {cells}
                    <div className="coordinate">{String.fromCharCode(65 + row)}</div> {/* Right side coordinates */}
                </div>
            );
        }
        return board;
    };

    const renderTopCoordinates = () => {
        let topCoords = [];
        for (let col = 0; col < cols; col++) {
            topCoords.push(
                <div key={`top-${col}`} className="coordinate">{9 - col}</div>
            );
        }
        topCoords.push(<div key="top-right" className="coordinate" />); // Top right corner
        return <div className="row coordinates-row">{topCoords}</div>;
    };

    return (
        <div className="board-container">
            {renderTopCoordinates()}
            <div className="board">{renderBoard()}</div>
            <div className="move-input">
                <input
                    type="text"
                    value={move}
                    onChange={(e) => setMove(e.target.value)}
                    placeholder="e.g., 7g7f"
                />
                <button onClick={handleMoveSubmit}>Submit Move</button>
            </div>
        </div>
    );
};

export default ShogiBoard;
