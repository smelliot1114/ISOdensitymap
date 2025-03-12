import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# ====== Load Data ======
density_map_data = pd.read_csv("DensityMapDataV2_Cleaned.csv")

# ====== State Abbreviations Mapping ======
state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "Washington, D.C.": "DC"
}

# Apply state abbreviation mapping if not already present
if "state_abbrev" not in density_map_data.columns:
    density_map_data["state_abbrev"] = density_map_data["state_name"].map(state_abbrev)

# ====== AI Job Density Map ======
fig_density = px.choropleth(
    density_map_data,
    locations="state_abbrev",
    locationmode="USA-states",
    color="count",
    hover_name="state_name",
    hover_data={"count": True, "percent": True},
    color_continuous_scale="Blues",
    scope="usa",
    title="AI Job Density by State"
)

fig_density.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>AI Job Count: %{customdata[0]:,.0f}<br>Percentage of AI Listings: %{customdata[1]:.2f}%<extra></extra>"
)

# ====== Dash App ======
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AI Job Market Density Map", style={"textAlign": "center", "color": "#ffffff", "fontFamily": "Arial, sans-serif"}),
    dcc.Graph(figure=fig_density)
], style={"backgroundColor": "#3a3a3a", "padding": "20px", "fontFamily": "Arial, sans-serif"})

server = app.server

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Default to 8050 if PORT not set
    app.run_server(debug=True, host="0.0.0.0", port=port)

