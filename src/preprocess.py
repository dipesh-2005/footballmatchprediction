from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_match_data():

    # Load dataset
    df = pd.read_csv(DATA_DIR / "teams_match_features.csv")


    # Create winner column
    df["winner"] = np.where(
        df["home_goals"] > df["away_goals"],
        "Home",
        np.where(
            df["home_goals"] < df["away_goals"],
            "Away",
            "Draw"
        )
    )

    # Remove unused column
    df.drop(columns=["is_world_cup"], inplace=True)

    # Create a copy
    df_clean = df.copy()

    # Remove columns not used for training
    df_clean.drop(
        columns=[
            "_home_team",
            "_away_team",
            "_date",
            "_tournament"
        ],
        inplace=True
    )

    # Fill missing values
    missing_columns = [
        "home_avg_pace",
        "home_avg_shooting",
        "home_avg_passing",
        "away_avg_pace",
        "away_avg_shooting",
        "away_avg_passing"
    ]

    for col in missing_columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())

    return df, df_clean