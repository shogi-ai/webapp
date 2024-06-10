import React from 'react';
import ShogiBoard from './components/ShogiBoard'
import './App.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>Shogi Board</h1>
      <ShogiBoard />
    </div>
  );
};

export default App;
