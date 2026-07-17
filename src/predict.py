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

# Convert label to actual team name
    if winner == "Home":
      winner = home_team
    elif winner == "Away":
      winner = away_team
    else:
      winner = "Draw"

    # -----------------------------------
    # Winner probabilities
    # -----------------------------------
    probs = winner_model.predict_proba(X_winner)[0]

    classes = label_encoder.inverse_transform(
        list(range(len(probs)))
    )

    probabilities = {}

    for cls, prob in zip(classes, probs):
        if cls == "Home":
            probabilities[home_team] = round(float(prob), 3)
        elif cls == "Away":
            probabilities[away_team] = round(float(prob), 3)
        else:
            probabilities["Draw"] = round(float(prob), 3)
    # Maximum win probability
    max_probability = max(probabilities.values())
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
# Make score consistent with winner
# -----------------------------------

    if winner == home_team:

        if home_goals <= away_goals:
            home_goals = away_goals + 1

    # Increase goals if confidence is high
        if max_probability >= 0.95:
            home_goals = max(home_goals, 4)

        elif max_probability >= 0.85:
            home_goals = max(home_goals, 3)

        elif max_probability >= 0.70:
            home_goals = max(home_goals, 2)


    elif winner == away_team:

        if away_goals <= home_goals:
            away_goals = home_goals + 1

        if max_probability >= 0.95:
            away_goals = max(away_goals, 4)

        elif max_probability >= 0.85:
            away_goals = max(away_goals, 3)

        elif max_probability >= 0.70:
            away_goals = max(away_goals, 2)


    else:

        if home_goals > away_goals:
            away_goals = home_goals

        elif away_goals > home_goals:
            home_goals = away_goals
    

    # -----------------------------------
    # Return result
    # -----------------------------------
    return {
    "match": f"{home_team} vs {away_team}",
    "winner": winner,
    "score": f"{home_team} {home_goals} - {away_goals} {away_team}",
    "home_goals": home_goals,
    "away_goals": away_goals,
    "probabilities": probabilities
}