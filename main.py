import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="NutriChef AI - Dual Mode")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset and trained models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

food_df = pd.read_csv(os.path.join(BASE_DIR, "food_nutrition.csv"))
food_df.columns = food_df.columns.str.strip()

calorie_model = joblib.load(
    os.path.join(BASE_DIR, "nutrichef_real_model.joblib")
)

protein_model = joblib.load(
    os.path.join(BASE_DIR, "nutrichef_protein_model.joblib")
)

client = genai.Client()


class RecipeRequest(BaseModel):
    ingredients: str


# Match user ingredients with dataset entries
def find_matching_ingredients(user_input):
    raw_ingredients = user_input.lower().split(",")
    matched_row_indexes = []

    for ingredient in raw_ingredients:
        clean_ingredient = ingredient.strip()

        if not clean_ingredient:
            continue

        for index, row in food_df.iterrows():
            if clean_ingredient in str(row["food_normalized"]).lower():
                matched_row_indexes.append(index)
                break

    return matched_row_indexes


@app.post("/api/recipe")
async def get_recipe(request: RecipeRequest):
    if not request.ingredients.strip():
        raise HTTPException(
            status_code=400,
            detail="Empty ingredient query"
        )

    matched_indexes = find_matching_ingredients(
        request.ingredients
    )

    total_carbs = 0.0
    total_protein = 0.0
    total_fat = 0.0
    total_calories = 0.0
    resolved_names = []

    # Aggregate nutrition values
    if matched_indexes:
        for idx in matched_indexes:
            row = food_df.iloc[idx]

            total_carbs += float(
                pd.to_numeric(
                    row.get("Carbohydrates (g per 100g)"),
                    errors="coerce"
                ) or 0.0
            )

            total_protein += float(
                pd.to_numeric(
                    row.get("Protein (g per 100g)"),
                    errors="coerce"
                ) or 0.0
            )

            total_fat += float(
                pd.to_numeric(
                    row.get("Fat (g per 100g)"),
                    errors="coerce"
                ) or 0.0
            )

            total_calories += float(
                pd.to_numeric(
                    row.get("Calories (kcal per 100g)"),
                    errors="coerce"
                ) or 0.0
            )

            resolved_names.append(
                row.get("food_normalized", "Unknown Item")
            )

    else:
        total_carbs = 10.0
        total_protein = 5.0
        total_fat = 2.0
        total_calories = 120.0
        resolved_names = [request.ingredients]

    # Calorie prediction
    calorie_features = pd.DataFrame(
        [[total_carbs, total_protein, total_fat]],
        columns=[
            "Carbohydrates (g per 100g)",
            "Protein (g per 100g)",
            "Fat (g per 100g)"
        ]
    )

    predicted_calories = float(
        calorie_model.predict(calorie_features)[0]
    )

    final_calories = max(
        round(predicted_calories, 1),
        0.0
    )

    # Protein prediction
    protein_features = pd.DataFrame(
        [[total_carbs, total_calories, total_fat]],
        columns=[
            "Carbohydrates (g per 100g)",
            "Calories (kcal per 100g)",
            "Fat (g per 100g)"
        ]
    )

    predicted_protein = float(
        protein_model.predict(protein_features)[0]
    )

    final_protein = max(
        round(predicted_protein, 1),
        0.0
    )

    prompt = (
        f"Create a healthy recipe using strictly these items: "
        f"{', '.join(resolved_names)}. "
        f"Do not add extra ingredients."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        recipe_text = response.text

    except ClientError as api_error:
        if api_error.code == 429:
            recipe_text = (
                "Gemini API quota limit reached. "
                "Nutrition predictions are still available. "
                "Please try again later."
            )
        else:
            recipe_text = (
                f"AI service error: {api_error.message}"
            )

    except Exception:
        recipe_text = (
            "Network error while contacting AI service."
        )

    return {
        "recipe_markdown": recipe_text,
        "estimated_calories": final_calories,
        "estimated_protein": final_protein,
        "debug_resolved_items": resolved_names
    }