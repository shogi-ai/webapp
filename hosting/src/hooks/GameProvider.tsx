import { doc, getDoc, getFirestore } from "firebase/firestore";
import { getFunctions, httpsCallable } from "firebase/functions";
import { ReactNode, createContext, useState } from "react";

interface Move {}

interface Game {
  uid: string;
  moves: Move[];
  board: (string | null)[][];
}

export interface GameContextType {
  currentGame: Game | null;
  loading: boolean;
  get: () => Promise<void>;
  get_by_id: (uid: string) => Promise<void>;
  create: () => Promise<void>;
  get_legal_moves: (
    from_square: string
  ) => Promise<(string | null)[][] | undefined>;
}

export const GameContext = createContext<GameContextType | undefined>(
  undefined
);

interface Props {
  children: ReactNode;
}

export const GameProvider = ({ children }: Props) => {
  const db = getFirestore();
  const functions = getFunctions();

  const [currentGame, setCurrentGame] = useState<Game | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const rootCollection = "games";

  const make_table = (board_list: [string | null]) => {
    const result = [];
    for (let i = 0; i < 81; i += 9) {
      result.push(board_list.slice(i, i + 9));
    }
    return result;
  };

  const _get_by_id = async (uid: string): Promise<Game | null> => {
    const gameRef = doc(db, rootCollection, uid);
    const gameDoc = await getDoc(gameRef);
    if (gameDoc.exists()) {
      const gameData = gameDoc.data();
      gameData.board = make_table(gameData.board);
      return gameData as Game;
    }
    return null;
  };

  const get = async (): Promise<void> => {
    setLoading(true);
    try {
      const uid = localStorage.getItem("gameUID");
      if (uid) {
        const game = await _get_by_id(uid);
        if (game !== null) {
          setCurrentGame(game);
        }
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const get_by_id = async (uid: string): Promise<void> => {
    setLoading(true);
    try {
      const game = await _get_by_id(uid);
      if (game !== null) {
        setCurrentGame(game);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const create = async (): Promise<void> => {
    setLoading(true);
    try {
      //
      localStorage.removeItem("gameUID");
      setCurrentGame(null);

      // Create new game
      const createGame = httpsCallable(functions, "create_game");
      const result = await createGame();
      const uid: string = result.data as string;

      // Update local storage
      localStorage.setItem("gameUID", uid);

      // Update current state
      const game = await _get_by_id(uid);
      if (game !== null) {
        setCurrentGame(game);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const get_legal_moves = async (from_square: string) => {
    setLoading(true);
    try {
      const getLegalMoves = httpsCallable(functions, "read_legal_moves");
      const response = await getLegalMoves({ from_square });
      return response.data as (string | null)[][];
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const contextValue: GameContextType = {
    currentGame,
    loading,
    get,
    get_by_id,
    create,
    get_legal_moves,
  };

  return (
    <GameContext.Provider value={contextValue}>{children}</GameContext.Provider>
  );
};
