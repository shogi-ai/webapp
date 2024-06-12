import "./Piece.css";

interface PieceProps {
  symbol: string;
  isBlack: boolean;
}

const Piece: React.FC<PieceProps> = ({ symbol, isBlack }) => {
  return <div className={`piece ${isBlack ? "black" : "white"}`}>{symbol}</div>;
};

export default Piece;
