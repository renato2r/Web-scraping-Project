import streamlit as st
import pandas as pd
import altair as alt

# Load the cleaned dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/clean/hr_leaders_by_team_clean.csv")

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
selected_league = st.sidebar.selectbox("Select League", ["All", "AL", "NL"])
selected_year = st.sidebar.slider("Select Year", int(df["Year"].min()), int(df["Year"].max()), step=1)
min_hr, max_hr = int(df["HR"].min()), int(df["HR"].max())
selected_hr = st.sidebar.slider("Minimum Home Runs", min_hr, max_hr, value=min_hr)

st.sidebar.markdown("---")
ranking_mode = st.sidebar.selectbox(
    "Top 10 HR Leaders View",
    ["All-Time", "By League", "By Decade"]
)


# Filter the dataset
filtered_df = df[df["Year"] == selected_year]
if selected_league != "All":
    filtered_df = filtered_df[filtered_df["League"] == selected_league]
filtered_df = filtered_df[filtered_df["HR"] >= selected_hr]

# Main title
st.title("MLB Home Run Leaders by Team")

# 1. Table display
st.subheader(f"Top HR Leaders in {selected_year}")
top_df = filtered_df.sort_values("HR", ascending=False).head(2)
st.dataframe(top_df, use_container_width=True)


# 2. Bar chart of HRs by player
st.subheader("Home Runs by Player")
bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("HR:Q", title="Home Runs"),
    y=alt.Y("Player:N", sort='-x', title="Player"),
    color="League:N"
).properties(width=700, height=400)
st.altair_chart(bar_chart, use_container_width=True)

# 3. Line chart over time (aggregated)
st.subheader("Average Home Runs per Year")
avg_hr_df = df.groupby("Year")["HR"].mean().reset_index()
line_chart = alt.Chart(avg_hr_df).mark_line().encode(
    x="Year:O",
    y=alt.Y("HR:Q", title="Average HRs"),
).properties(width=700, height=400)
st.altair_chart(line_chart, use_container_width=True)

#4.  Top 10 HR Leaders
st.subheader("Top 10 HR Leaders")

# Helper function to calculate decade
def get_decade(year):
    return f"{int(year) // 10 * 10}s"

# Apply filter based on user selection
if ranking_mode == "All-Time":
    temp_df = df.copy()
    title_suffix = "All-Time"

elif ranking_mode == "By League":
    selected_league_rank = st.sidebar.radio("Select League", ["AL", "NL"], horizontal=True)
    temp_df = df[df["League"] == selected_league_rank]
    title_suffix = f"{selected_league_rank} League"

elif ranking_mode == "By Decade":
    df["Decade"] = df["Year"].apply(get_decade)
    available_decades = sorted(df["Decade"].unique())
    selected_decade = st.sidebar.selectbox("Select Decade", available_decades)
    temp_df = df[df["Decade"] == selected_decade]
    title_suffix = f"{selected_decade}"

# Aggregate HRs only by player (not by team)
agg_df = temp_df.groupby("Player", as_index=False)["HR"].sum()
top10 = agg_df.sort_values("HR", ascending=False).head(10)
top10["Rank"] = range(1, len(top10) + 1)
top10["Label"] = top10["Rank"].astype(str) + ". " + top10["Player"]

# Build bar chart (no team tooltip)
# Vertical bar chart with individual colors
chart = alt.Chart(top10).mark_bar().encode(
    x=alt.X("Label:N", sort='-y', title="Player"),
    y=alt.Y("HR:Q", title="Total Home Runs"),
    color=alt.Color("Player:N", legend=None),  # Unique color per player
    tooltip=["Player", "HR"]
).properties(
    title=f"Top 10 Home Runs Leaders – {title_suffix}",
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)

# 5. Aggregation by team
st.subheader("Top Teams by Total Home Runs (All Years)")

# Aggregate total HRs by team (across all years)
team_hr_all = df.groupby("Team", as_index=False)["HR"].sum().sort_values(by="HR", ascending=False).head(10)

team_bar = alt.Chart(team_hr_all).mark_bar().encode(
    x=alt.X("HR:Q", title="Total Home Runs"),
    y=alt.Y("Team:N", sort='-x', title="Team"),
    tooltip=["HR"]
).properties(width=700, height=400)

st.altair_chart(team_bar, use_container_width=True)


