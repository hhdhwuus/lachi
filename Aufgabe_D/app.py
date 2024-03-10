import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from dash import callback_context

# Daten laden und vorverarbeiten

data_path = '../ProcessedData/combined_tage.csv'
data = pd.read_csv(data_path)

# Datum einmalig konvertieren
data['datum'] = pd.to_datetime(data['datum'])

# Vorverarbeitung: Eindeutige Liste der Zählstellen
zaehlstellen_liste = data['zaehlstelle'].unique()

# App initialisieren
app = dash.Dash(__name__)


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

operation_dropdown = dcc.Dropdown(
    id='operation-dropdown',
    options=[
        {'label': 'Mean', 'value': 'Mean'},
        {'label': 'Sum', 'value': 'Sum'}
    ],
    value='Sum',
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
        html.H2(id="calculation-h2", children="Calculation"),
        html.P(id="calculation-p", children="Select statistic operation"),
        html.Div(id="operation-dropdown-div", children=operation_dropdown),
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
                    "yaxis": {"showgrid": True, "showline": False},
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

# Callbacks Calculation


@app.callback(
    [Output('operation-dropdown-div', 'style'),
     Output('calculation-h2', 'style'),
     Output('calculation-p', 'style')],
    [Input('interval-dropdown', 'value')]
)
def toggle_operation_dropdown(interval_value):
    if interval_value == 'Day':
        # Verstecke die Elemente, wenn 'Day' ausgewählt ist
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}]
    else:
        # Zeige die Elemente ansonsten an
        return [{'display': 'block'}, {'display': 'block'}, {'display': 'block'}]


# Callbacks Dropdown
@app.callback(
    Output('chart-graph', 'figure'),
    [Input('station-dropdown', 'value'),
     Input('operation-dropdown', 'value'),
     Input('interval-dropdown', 'value')]
)
def update_graph(selected_zaehlstelle, selected_operation, selected_interval):
    filtered_data = data[data['zaehlstelle'] == selected_zaehlstelle]

    if selected_operation == "Sum":
        if selected_interval == 'Day':
            # Tägliche Daten aggregieren, wenn nicht bereits geschehen
            aggregated_data = filtered_data.groupby(filtered_data['datum'].dt.date)[
                'gesamt'].sum().reset_index(name='gesamt')
            fig = px.line(aggregated_data, x='datum', y='gesamt',
                          title=f"Täglicher Verlauf: {selected_zaehlstelle}")
        else:
            # Jährliche Daten aggregieren
            aggregated_data = filtered_data.groupby(filtered_data['datum'].dt.year)[
                'gesamt'].sum().reset_index(name='gesamt')
            fig = px.line(aggregated_data, x='datum', y='gesamt',
                          title=f"Jährlicher Verlauf: {selected_zaehlstelle}")
    elif selected_operation == "Mean":
        if selected_interval == 'Day':
            # Tägliche Daten aggregieren, wenn nicht bereits geschehen
            aggregated_data = filtered_data.groupby(filtered_data['datum'].dt.date)[
                'gesamt'].mean().reset_index(name='gesamt')
            fig = px.line(aggregated_data, x='datum', y='gesamt',
                          title=f"Täglicher Verlauf: {selected_zaehlstelle}")
        else:
            # Jährliche Daten aggregieren
            aggregated_data = filtered_data.groupby(filtered_data['datum'].dt.year)[
                'gesamt'].mean().reset_index(name='gesamt')
            fig = px.line(aggregated_data, x='datum', y='gesamt',
                          title=f"Jährlicher Verlauf: {selected_zaehlstelle}")

    fig.add_hline(y=0, line_color="white", line_width=1)

    fig.update_layout(plot_bgcolor="#0F1117",
                      paper_bgcolor="#0F1117", font={"color": "white", 'size': 20}, xaxis=dict(
                          title="Datum",
                      ),
                      yaxis=dict(
                          title="Anzahl der Fahrten",
                      ))

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
