import streamlit as st

from src.feature_builder import get_all_teams
from src.predict import predict_match


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Football Match Predictor",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
<style>

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* App background */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}

/* Title */
h1{
    text-align:center;
    color:white;
    font-weight:800;
}

/* Subtitle */
p{
    color:#d1d5db;
}

/* Metric Cards */
[data-testid="stMetric"]{
    background:#1f2937;
    border-radius:15px;
    padding:18px;
    border:1px solid #374151;
    box-shadow:0px 5px 20px rgba(0,0,0,.35);
}

/* Buttons */
.stButton>button{
    background:#16a34a;
    color:white;
    border-radius:12px;
    height:55px;
    width:100%;
    font-size:18px;
    font-weight:bold;
    border:none;
}

.stButton>button:hover{
    background:#15803d;
}

/* Select boxes */
[data-baseweb="select"]{
    background:#1f2937;
    border-radius:10px;
}

/* Progress bar */
.stProgress > div > div > div > div{
    background:#22c55e;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Title
# --------------------------------------------------
st.markdown(
    """
<h1>⚽ Football Match Predictor</h1>

<p style="text-align:center;font-size:20px;">
Predict international football matches using Machine Learning
</p>
""",
unsafe_allow_html=True
)




st.divider()

# --------------------------------------------------
# Load Teams
# --------------------------------------------------
teams = get_all_teams()

# --------------------------------------------------
# Team Selection
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox(
        "🏠 Home Team",
        teams,
        index=teams.index("Argentina") if "Argentina" in teams else 0
    )

with col2:
    away_team = st.selectbox(
        "✈ Away Team",
        teams,
        index=teams.index("Brazil") if "Brazil" in teams else 1
    )

# --------------------------------------------------
# Tournament
# --------------------------------------------------
tournament = st.selectbox(
    "🏆 Tournament",
    [
        "Friendly",
        "FIFA World Cup",
        "UEFA Euro",
        "Copa América",
        "AFC Asian Cup",
        "Africa Cup of Nations"
    ]
)

# --------------------------------------------------
# Neutral Venue
# --------------------------------------------------
is_neutral = st.checkbox("🏟 Neutral Venue")

st.divider()

# --------------------------------------------------
# Predict Button
# --------------------------------------------------
if st.button("🔮 Predict Match"):

    if home_team == away_team:

        st.error("❌ Home Team and Away Team cannot be the same.")

    else:

        with st.spinner("Predicting match..."):

            st.session_state["result"] = predict_match(
                home_team=home_team,
                away_team=away_team,
                tournament=tournament,
                is_neutral=is_neutral
            )

# --------------------------------------------------
# Display Result
# --------------------------------------------------
if "result" in st.session_state:

    result = st.session_state["result"]

    st.success("Prediction Complete!")

    st.divider()

    st.markdown(f"# {result['match']}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="🏆 Predicted Winner",
            value=result["winner"]
        )

    with col2:
        st.metric(
            label="⚽ Predicted Score",
            value=result["score"]
        )

    st.divider()

    st.subheader("📊 Winning Probabilities")

    for team, probability in result["probabilities"].items():

        st.write(f"### {team}")

        st.progress(float(probability))

        st.caption(f"{probability * 100:.1f}%")