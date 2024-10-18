import { useState } from "react";
import "./App.css";
import RecipeList from "./Components/RecipeList";
function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <RecipeList />
    </div>
  );
}

export default App;
