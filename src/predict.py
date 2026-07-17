from src.model_loader import load_models
from src.feature_builder import build_features

# Load models once
winner_model, home_model, away_model, label_encoder = load_models()


def predict_match(home_team, away_team, tournament, is_neutral):

    # -----------------------------------
    # Build features (29 features)
    # -----------------------------------
    X = build_features(
        home_team=home_team,
        away_team=away_team,
        tournament=tournament,
        is_neutral=is_neutral
    )

    # -----------------------------------
    # Winner model expects 28 features
    # Remove is_world_cup
    # -----------------------------------
    X_winner = X.drop(columns=["is_world_cup"])

    # -----------------------------------
    # Goal models expect 29 features
    # -----------------------------------
    X_goals = X.copy()

    # -----------------------------------
    # Winner prediction
    # -----------------------------------
    winner_encoded = winner_model.predict(X_winner)[0]

    winner = label_encoder.inverse_transform([winner_encoded])[0]

    # -----------------------------------
    # Winner probabilities
    # -----------------------------------
    probs = winner_model.predict_proba(X_winner)[0]

    classes = label_encoder.inverse_transform(
        list(range(len(probs)))
    )

    probabilities = {
        cls: round(float(prob), 3)
        for cls, prob in zip(classes, probs)
    }

    # -----------------------------------
    # Goal prediction
    # -----------------------------------
    home_goals = round(
        float(home_model.predict(X_goals)[0])
    )

    away_goals = round(
        float(away_model.predict(X_goals)[0])
    )

    # -----------------------------------
    # Return result
    # -----------------------------------
    return {
        "home_team": home_team,
        "away_team": away_team,
        "winner": winner,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "probabilities": probabilities
    }