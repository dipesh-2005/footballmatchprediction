from pathlib import Path
import joblib

# Get the project root (footballmatchesprediction)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# models folder
MODELS_DIR = PROJECT_ROOT / "models"


def load_models():
    winner_model = joblib.load(MODELS_DIR / "winner_prediction_model.pkl")
    home_goals_model = joblib.load(MODELS_DIR / "home_goals_model.pkl")
    away_goals_model = joblib.load(MODELS_DIR / "away_goals_model.pkl")
    label_encoder = joblib.load(MODELS_DIR / "label_encoder.pkl")

    return winner_model, home_goals_model, away_goals_model, label_encoder