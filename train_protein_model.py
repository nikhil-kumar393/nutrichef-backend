import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

print("Loading nutrition dataset...")
df = pd.read_csv("food_nutrition.csv")

df.columns = df.columns.str.strip()


X_columns = ["Carbohydrates (g per 100g)", "Calories (kcal per 100g)", "Fat (g per 100g)"]
y_column = "Protein (g per 100g)"

df = df.dropna(subset=X_columns + [y_column])

X = df[X_columns]
y = df[y_column]

print(f" Training Protein predictor model on {len(df)} rows...")
protein_model = LinearRegression()
protein_model.fit(X, y)

# Save it as a distinct file
joblib.dump(protein_model, "nutrichef_protein_model.joblib")
print(" Protein model saved successfully as 'nutrichef_protein_model.joblib'!")