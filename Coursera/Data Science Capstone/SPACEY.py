# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div([dcc.Dropdown(id='site-dropdown', 
                                                        options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        ],
                                                        value='ALL',
                                                        placeholder='Select a Launch Site here',
                                                        searchable=True,
                                                        style={'width':'95%', 'padding':3, 'font_size':20, 'textAlign': 'center'})
                                    # Place them next to each other using the division style
                                            ], style={'display':'flex'}),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(site):

    filtered_df = spacex_df[['Launch_Site', 'class']]
    filtered_df = filtered_df[filtered_df['class']!= 0]
    if site == 'ALL':
        fig = px.pie(filtered_df, 
                        values='class', 
                        names='Launch_Site', 
                        title='Total Success Launches by Site',
                        color_discrete_sequence=px.colors.sequential.RdBu)
        return fig
    
    else:
        edata = spacex_df[spacex_df['Launch_Site']==site]
        fig = px.pie(edata, 
                    names='class',
                    title=f'Total Success Launches for {site}',
                    color_discrete_sequence=px.colors.sequential.RdBu)
        
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(site, payload):
    if site == 'ALL':
        filter = spacex_df[['Launch_Site', 'Booster_Version_Category', 'class', 'Payload Mass (kg)']]
        filter2 = filter[(filter['Payload Mass (kg)']>= payload[0]) & (filter['Payload Mass (kg)']<= payload[1])]
        fig = px.scatter(filter2, 
                         x="Payload Mass (kg)", 
                         y="class", 
                         color="Booster_Version_Category", 
                         title='Correlation between Payload and Success for all Sites')
        
        return fig
    else:
        filter = spacex_df[['Launch_Site', 'Booster_Version_Category', 'class', 'Payload Mass (kg)']]
        filter2 = filter[filter['Launch_Site']==site]
        filter3 = filter2[(filter2['Payload Mass (kg)']>= payload[0]) & (filter2['Payload Mass (kg)']<= payload[1])]
        fig = px.scatter(filter3, 
                         x="Payload Mass (kg)", 
                         y="class", 
                         color="Booster_Version_Category", 
                         title=f'Correlation between Payload and Success for {site}')

        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()