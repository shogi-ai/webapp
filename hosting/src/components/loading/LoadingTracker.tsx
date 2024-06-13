import { useGame } from "../../hooks/useGame";
import { Loading } from "./Loading";
import "./LoadingTracker.css";

export const LoadingTracker = () => {
  const { loading: loadingGame } = useGame();

  return (
    <>
      {loadingGame === true ? (
        <div className="loading-tracker-container">
          <div className="loading-tracker-content">
            {loadingGame === true && <Loading description={"Loading Game"} />}
          </div>
        </div>
      ) : (
        <></>
      )}
    </>
  );
};
