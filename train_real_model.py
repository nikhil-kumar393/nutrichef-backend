import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

print("Loading your nutrition spreadsheet...")
df = pd.read_csv("food_nutrition.csv")

X_columns = ["Carbohydrates (g per 100g)", "Protein (g per 100g)", "Fat (g per 100g)"]
y_column = "Calories (kcal per 100g)"

df = df.dropna(subset=X_columns + [y_column])

X = df[X_columns]
y = df[y_column]

print(f" Training calorie predictor model on {len(df)} rows...")

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "nutrichef_real_model.joblib")
print("Model trained successfully as nutrichef_real_model.joblib!")