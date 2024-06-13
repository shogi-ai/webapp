import ShogiBoard from "../components/ShogiBoard";

import "../App.css";
import { useGame } from "../hooks/useGame";
import { useEffect } from "react";

export const Shogi = () => {
  const { currentGame, get, create } = useGame();

  useEffect(() => {
    console.log("get game data");
    get();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="App">
      {currentGame ? (
        <>
          <h1>Shogi Board</h1>
          <ShogiBoard />
        </>
      ) : (
        <>
          <button className="create-game-button" onClick={create}>
            Create Game
          </button>
        </>
      )}
    </div>
  );
};
