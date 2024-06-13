import { ShogiBoard } from "../components/ShogiBoard";

import "../App.css";
import { useGame } from "../hooks/useGame";
import { useEffect } from "react";
import { Loading } from "../components/loading/Loading";

export const Shogi = () => {
  const { currentGame, get, create, loading } = useGame();

  useEffect(() => {
    get();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="App">
      {currentGame ? (
        <>
          <h1>Shogi Board</h1>
          <ShogiBoard />
          <button className="restart-game-button" onClick={create}>
            Restart Game
          </button>
        </>
      ) : (
        <>
          <button className="create-game-button" onClick={create}>
            Create Game
          </button>
        </>
      )}
      {loading && <Loading description={"Game is loading"} />}
    </div>
  );
};
