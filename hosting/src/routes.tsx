import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Shogi } from "./pages/shogi";

export const Routing = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="*" element={<Shogi />} />
      </Routes>
    </BrowserRouter>
  );
};
