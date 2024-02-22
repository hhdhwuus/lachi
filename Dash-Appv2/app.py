import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_daq as daq
import plotly.express as px
from dash import callback_context

data_path = r'C:\Users\Jonas\Desktop\Integrationsseminar\FahrradMuenchen\combined_tage.csv'
data = pd.read_csv(data_path)

# Vorverarbeitung: Eindeutige Liste der Zählstellen
zaehlstellen_liste = data['zaehlstelle'].unique()

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)


# Side panel
station_dropdown = dcc.Dropdown(
    id='station-dropdown',
    options=[{'label': zaehlstelle, 'value': zaehlstelle}
             for zaehlstelle in zaehlstellen_liste],
    value=zaehlstellen_liste[0],
    clearable=False,
)

interval_dropdown = dcc.Dropdown(
    id='interval-dropdown',
    options=[
        {'label': 'Year', 'value': 'Year'},
        {'label': 'Day', 'value': 'Day'}
    ],
    value='Year',
    clearable=False,
)

chart_description = html.H2(id="chart-description", children="")

side_panel_layout = html.Div(
    id="panel-side",
    children=[
        html.H1(children="Controls"),
        html.H2(id="station-h2", children="Station"),
        html.P(children="Choose Station to view data"),
        html.Div(id="station-dropdown-div", children=station_dropdown),
        html.H2(id="interval-h2", children="Interval"),
        html.P(children="Select data interval"),
        html.Div(id="interval-dropdown-div", children=interval_dropdown),
    ],
)

# chart
chart = html.Div(
    id="chart-container",
    children=[
        html.H1(children="Fahrradstatistik München"),
        chart_description,
        dcc.Graph(
            id="chart-graph",
            figure={
                "layout": {
                    "margin": {"t": 30, "r": 35, "b": 40, "l": 50},
                    "xaxis": {"dtick": 1, "gridcolor": "#636363", "showline": False},
                    "yaxis": {"showgrid": True},
                    "plot_bgcolor": "#0F1117",
                    "paper_bgcolor": "#0F1117",
                    "font": {"color": "gray"},
                },
            },
            config={"displayModeBar": True},
        ),
    ],
)

# Control panel + map
main_panel_layout = html.Div(
    id="panel-upper-lower",
    children=[
        html.Div(
            id="panel",
            children=[
                chart
            ],
        ),
    ],
)

# Root
root_layout = html.Div(
    id="root",
    children=[
        side_panel_layout,
        main_panel_layout,
    ],
)

app.layout = root_layout


# Callbacks Dropdown
@app.callback(
    [Output('chart-graph', 'figure'),
     Output('chart-description', 'children')],
    [Input('station-dropdown', 'value'),
     Input('interval-dropdown', 'value')]
)
def update_graph(selected_zaehlstelle, selected_interval):
    filtered_data = data[data['zaehlstelle'] == selected_zaehlstelle]
    filtered_data['datum'] = pd.to_datetime(filtered_data['datum'])
    print(filtered_data)
    yearly_counts = filtered_data.groupby(filtered_data['datum'].dt.year)[
        'gesamt'].sum().reset_index()
    fig = px.line(filtered_data, x='datum', y='gesamt')

    # Anpassen des Layouts
    fig.update_layout(
        margin={"t": 30, "r": 35, "b": 40, "l": 50},
        xaxis={"dtick": 800, "gridcolor": "#636363", "showline": True},
        yaxis={"showgrid": False, "showline": True},
        plot_bgcolor="#0F1117",
        paper_bgcolor="#0F1117",
        font={"color": "white"},
    )
    print(selected_interval)
    description_text = f"Täglicher Verlauf der Zählungen: {selected_zaehlstelle}"

    return fig, description_text


if __name__ == "__main__":
    app.run_server(debug=True)
