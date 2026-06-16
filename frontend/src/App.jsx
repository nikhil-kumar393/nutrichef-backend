
import React, { useState } from 'react';
import {
  ChefHat,
  Flame,
  ListMinus,
  Loader2,
  Sparkles,
  Dumbbell
} from 'lucide-react';
import './App.css';

function App() {
  const [ingredients, setIngredients] = useState('');
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!ingredients.trim()) return;

    setLoading(true);
    setError('');
    setRecipe(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/recipe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          accept: 'application/json',
        },
        body: JSON.stringify({
          ingredients: ingredients
        }),
      });

      if (!response.ok) {
        throw new Error('Backend server returned an error');
      }

      const data = await response.json();
      setRecipe(data);

    } catch (err) {
      setError('Failed to connect to the backend API server. Make sure FastAPI is running!');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="app-wrapper">

        <header className="app-header">
          <div className="header-title-container">
            <ChefHat size={44} color="#f97316" />
            <h1 className="header-title">NutriChef AI</h1>
          </div>
          <p className="header-subtitle">AI Recipe Maker & Nutrition Analyzer</p>
        </header>

        <div className="form-card">
          <form onSubmit={handleSubmit}>

            <div style={{ marginBottom: '1.5rem' }}>
              <label className="input-label">Enter available ingredients:</label>
              <input
                type="text"
                value={ingredients}
                onChange={(e) => setIngredients(e.target.value)}
                placeholder="e.g., oats, banana, milk, peanut butter"
                className="ingredients-input"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="submit-btn"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin" size={20} />
                  Cooking with AI...
                </>
              ) : (
                <>
                  <Sparkles size={20} />
                  Generate AI Recipe & Predict Metrics
                </>
              )}
            </button>

          </form>

          {error && <p className="error-message">{error}</p>}
        </div>

        {recipe && (
          <div className="results-layout">

            <div className="macros-grid">

              <div className="calorie-card">
                <div>
                  <h3 className="calorie-label">Total Calories</h3>
                  <p className="calorie-value">{recipe.estimated_calories} kcal</p>
                </div>
                <Flame size={40} color="#f97316" />
              </div>

              <div className="protein-card">
                <div>
                  <h3 className="protein-label">Total Protein</h3>
                  <p className="protein-value">{recipe.estimated_protein} g</p>
                </div>
                <Dumbbell size={40} color="#26E864" />
              </div>

            </div>

            <div className="recipe-card">
              <div className="recipe-header">
                <ListMinus color="#26E864" size={24} />
                <h2>Your Custom AI Recipe</h2>
              </div>

              <div className="recipe-content">
                <pre
                  style={{
                    whiteSpace: 'pre-wrap',
                    fontFamily: 'inherit',
                    color: 'inherit',
                    margin: 0,
                    lineHeight: 'inherit',
                  }}
                >
                  {recipe.recipe_markdown}
                </pre>
              </div>

            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;

