import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

app = dash.Dash(__name__)

# Layout definition
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    
    dcc.Dropdown(id='site-dropdown', 
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL', placeholder="Select a Launch Site"),
    
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[0, 10000]),
    
    dcc.Graph(id='success-pie-chart'),
    dcc.Graph(id='success-payload-scatter-chart')
])

# Callbacks definition
@app.callback(Output('success-pie-chart', 'figure'), 
              Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    # Function to update pie chart based on site selection
    filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site] if selected_site != 'ALL' else spacex_df
    success_rate = filtered_df.groupby('class').size().reset_index(name='count')
    fig = px.pie(success_rate, values='count', names='class', title=f'Success Rate for {selected_site}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
