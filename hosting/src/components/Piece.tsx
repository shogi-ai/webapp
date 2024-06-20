import "./Piece.css";

interface PieceProps {
  symbol: string;
  isBlack: boolean;
  onClick?: any;
}

const Piece: React.FC<PieceProps> = ({ symbol, isBlack, onClick }) => {
  return (
    <div className={`piece ${isBlack ? "black" : "white"}`} onClick={onClick}>
      {symbol}
    </div>
  );
};

export default Piece;
