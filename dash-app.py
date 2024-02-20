import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data_path = r'C:\Users\Jonas\Desktop\Integrationsseminar\FahrradMuenchen\combined_tage.csv'
data = pd.read_csv(data_path)

# Vorverarbeitung: Eindeutige Liste der Zählstellen
zaehlstellen_liste = data['zaehlstelle'].unique()

# Dash-App initialisieren
app = dash.Dash(__name__)

# App-Layout
app.layout = html.Div([
    html.H1("Verlauf der Zählungen pro Zählstelle"),
    dcc.Dropdown(
        id='zaehlstelle-dropdown',
        options=[{'label': zaehlstelle, 'value': zaehlstelle} for zaehlstelle in zaehlstellen_liste],
        value=zaehlstellen_liste[0]  # Standardwert ist die erste Zählstelle
    ),
    dcc.Graph(id='zaehlungen-graph')
])

# Callback, um das Diagramm basierend auf der ausgewählten Zählstelle zu aktualisieren
@app.callback(
    Output('zaehlungen-graph', 'figure'),
    [Input('zaehlstelle-dropdown', 'value')]
)
def update_graph(selected_zaehlstelle):
    filtered_data = data[data['zaehlstelle'] == selected_zaehlstelle]
    filtered_data['datum'] = pd.to_datetime(filtered_data['datum'])
    yearly_counts = filtered_data.groupby(filtered_data['datum'].dt.year)['gesamt'].sum().reset_index()
    fig = px.line(yearly_counts, x='datum', y='gesamt', title=f'Jährlicher Verlauf der Zählungen: {selected_zaehlstelle}')
    return fig

# App starten
if __name__ == '__main__':
    app.run_server(debug=True)

