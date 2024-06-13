import { useEffect, useState } from "react";
import "./ShogiBoard.css";
import Piece from "./Piece";
import { useGame } from "../hooks/useGame";

export const ShogiBoard = () => {
  const { currentGame, get_legal_moves } = useGame();

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
    ["L", "N", "S", "G", "K", "G", "S", "N", "L"],
  ];

  useEffect(() => {
    if (currentGame !== null) {
      console.log(currentGame.board);
      setCurrentBoard(currentGame.board);
    }
  }, [currentGame]);

  const [move, setMove] = useState("");
  const [currentBoard, setCurrentBoard] =
    useState<(string | null)[][]>(initialBoard);
  const [blackCaptured] = useState<string[]>([]);
  const [whiteCaptured] = useState<string[]>([]);
  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);
  const [legalMoves, setLegalMoves] = useState<(string | null)[][]>([]);

  const pieceSymbols: { [key: string]: string } = {
    p: "歩",
    l: "香",
    n: "桂",
    s: "銀",
    g: "金",
    k: "王",
    r: "飛",
    b: "角",
    P: "歩",
    L: "香",
    N: "桂",
    S: "銀",
    G: "金",
    K: "玉",
    R: "飛",
    B: "角",
    "+p": "と",
    "+l": "杏",
    "+n": "圭",
    "+s": "全",
    "+r": "龍",
    "+b": "馬",
    "+P": "と",
    "+L": "杏",
    "+N": "圭",
    "+S": "全",
    "+R": "龍",
    "+B": "馬",
  };

  const handleMoveSubmit = () => {
    setMove("");
  };

  const handlePieceClick = async (row: number, col: number) => {
    const from_square = `${9 - col}${String.fromCharCode(
      65 + row
    ).toLowerCase()}`;
    setSelectedPiece(from_square);
    const moves = await get_legal_moves(from_square);
    if (moves !== undefined) setLegalMoves(moves);
  };

  const renderBoard = () => {
    const board = [];
    for (let row = 0; row < rows; row++) {
      const cells = [];
      for (let col = 0; col < cols; col++) {
        const piece = currentBoard[row][col];
        cells.push(
          <div
            key={`${row}-${col}`}
            className="cell"
            onClick={() => handlePieceClick(row, col)}
          >
            {piece && (
              <Piece
                symbol={pieceSymbols[piece]}
                isBlack={piece === piece.toLowerCase()}
              />
            )}
          </div>
        );
      }
      board.push(
        <div key={row} className="row">
          {cells}
          <div className="coordinate">{String.fromCharCode(65 + row)}</div>{" "}
          {/* Right side coordinates */}
        </div>
      );
    }
    return board;
  };

  const renderTopCoordinates = () => {
    const topCoords = [];
    for (let col = 0; col < cols; col++) {
      topCoords.push(
        <div key={`top-${col}`} className="coordinate">
          {9 - col}
        </div>
      );
    }
    topCoords.push(<div key="top-right" className="coordinate" />); // Top right corner
    return <div className="row coordinates-row">{topCoords}</div>;
  };

  const renderCapturedPieces = (captured: string[], isBlack: boolean) => {
    return (
      <div className="captured-pieces">
        {captured.map((piece, index) => (
          <Piece key={index} symbol={pieceSymbols[piece]} isBlack={isBlack} />
        ))}
      </div>
    );
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
      <div className="captured-container">
        <div className="black-captured">
          <h3>Black Captured</h3>
          {renderCapturedPieces(blackCaptured, true)}
        </div>
        <div className="white-captured">
          <h3>White Captured</h3>
          {renderCapturedPieces(whiteCaptured, false)}
        </div>
      </div>
    </div>
  );
};
