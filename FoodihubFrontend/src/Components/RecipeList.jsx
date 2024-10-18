// src/components/RecipeList.jsx
import React, { useEffect, useState } from "react";

const RecipeList = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true); // Add loading state
  const [error, setError] = useState(null); // Add error state

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/recipes/");

        console.log("Response Status:", response.status); // Log response status

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Fetched Data:", data); // Log the fetched data
        setRecipes(data);
      } catch (error) {
        console.error("Fetch error:", error); // Log the error
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  if (loading) {
    return <div>Loading...</div>; // Show loading message
  }

  if (error) {
    return <div>Error: {error}</div>; // Show error message
  }

  return (
    <div className="">
      <h1 className="text-2xl font-bold mb-4">Recipes</h1>
      <ul className="space-y-4">
        {recipes.map((recipe) => (
          <li key={recipe.id} className="border border-cyan-800 rounded-md p-4">
            <h2 className="text-xl font-semibold">{recipe.title}</h2>
            <p className="text-gray-700">{recipe.ingredients}</p>
            <p className="text-gray-700">{recipe.instructions}</p>
            <p className="text-yellow-600">Rating: {recipe.ratings}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RecipeList;
