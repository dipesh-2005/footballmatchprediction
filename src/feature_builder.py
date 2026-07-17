from pathlib import Path
import pandas as pd

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

# Load datasets once
player_df = pd.read_csv(DATA_DIR / "player_aggregates.csv")
team_form_df = pd.read_csv(DATA_DIR / "teams_form.csv")
match_df = pd.read_csv(DATA_DIR / "teams_match_features.csv")




def get_team_ratings(team):

    latest = (
        player_df[player_df["country"] == team]
        .sort_values("fifa_version")
        .iloc[-1]
    )

    return {
        "overall": latest["avg_overall"],
        "max_overall": latest["max_overall"],
        "attack": latest["avg_attack_overall"],
        "defense": latest["avg_defense_overall"],
        "pace": latest["avg_pace"],
        "shooting": latest["avg_shooting"],
        "passing": latest["avg_passing"]
    }



def get_team_form(team):

    latest = (
        team_form_df[team_form_df["team"] == team]
        .sort_values("match_date")
        .iloc[-1]
    )

    return {
        "goals_scored": latest["avg_goals_scored"],
        "goals_conceded": latest["avg_goals_conceded"],
        "win_rate": latest["win_rate"]
    }


def get_team_elo(team):

    # Home matches
    home = (
        match_df[match_df["_home_team"] == team][["_date", "home_elo"]]
        .rename(columns={"home_elo": "elo"})
    )

    # Away matches
    away = (
        match_df[match_df["_away_team"] == team][["_date", "away_elo"]]
        .rename(columns={"away_elo": "elo"})
    )

    # Combine both
    elo = pd.concat([home, away], ignore_index=True)

    # Convert date
    elo["_date"] = pd.to_datetime(elo["_date"])

    # Latest Elo
    latest = elo.sort_values("_date").iloc[-1]

    return latest["elo"]




def build_features(home_team, away_team, tournament, is_neutral):

    # -----------------------
    # Ratings
    # -----------------------
    home_rating = get_team_ratings(home_team)
    away_rating = get_team_ratings(away_team)

    # -----------------------
    # Form
    # -----------------------
    home_form = get_team_form(home_team)
    away_form = get_team_form(away_team)

    # -----------------------
    # Elo
    # -----------------------
    home_elo = get_team_elo(home_team)
    away_elo = get_team_elo(away_team)

    # -----------------------
    # Create dataframe
    # -----------------------
    features = {
        "home_elo": home_elo,
        "away_elo": away_elo,
        "elo_diff": home_elo - away_elo,

        "home_avg_overall": home_rating["overall"],
        "home_max_overall": home_rating["max_overall"],
        "home_avg_attack": home_rating["attack"],
        "home_avg_defense": home_rating["defense"],
        "home_avg_pace": home_rating["pace"],
        "home_avg_shooting": home_rating["shooting"],
        "home_avg_passing": home_rating["passing"],

        "away_avg_overall": away_rating["overall"],
        "away_max_overall": away_rating["max_overall"],
        "away_avg_attack": away_rating["attack"],
        "away_avg_defense": away_rating["defense"],
        "away_avg_pace": away_rating["pace"],
        "away_avg_shooting": away_rating["shooting"],
        "away_avg_passing": away_rating["passing"],

        "overall_diff": home_rating["overall"] - away_rating["overall"],
        "attack_diff": home_rating["attack"] - away_rating["attack"],
        "defense_diff": home_rating["defense"] - away_rating["defense"],

        "home_form_scored": home_form["goals_scored"],
        "home_form_conceded": home_form["goals_conceded"],
        "home_form_win_rate": home_form["win_rate"],

        "away_form_scored": away_form["goals_scored"],
        "away_form_conceded": away_form["goals_conceded"],
        "away_form_win_rate": away_form["win_rate"],

        "is_neutral": int(is_neutral),

        "is_world_cup": int(tournament == "FIFA World Cup"),

        "is_continental": int(
            tournament in [
                "UEFA Euro",
                "Copa América",
                "AFC Asian Cup",
                "Africa Cup of Nations",
                "CONCACAF Gold Cup"
            ]
        )

    }

    return pd.DataFrame([features])