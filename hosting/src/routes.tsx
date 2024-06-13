import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Shogi } from "./pages/shogi";
import { LoadingTracker } from "./components/loading/LoadingTracker";

export const Routing = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="*" element={<Shogi />} />
      </Routes>
      <LoadingTracker />
    </BrowserRouter>
  );
};
