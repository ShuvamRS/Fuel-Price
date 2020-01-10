import plotly.io as pio
import plotly
pio.templates.default = "none"
import plotly.graph_objs as go

import json
import re
from queries import getAnnualFuelPrices, get_schema


def get_states_from_region():
    region_dict = {
                'east coast (padd1)': {'maine', 'new hampshire', 'massachusetts', 'rhode island', 'connecticut', 'new york', 'new jersey', 'delaware', 'maryland', 'virginia', 'north carolina', 'south carolina', 'georgia', 'florida'},
                'new england (padd 1a)': {'maine', 'vermont', 'new hampshire', 'massachusetts', 'rhode island', 'connecticut'},
                'central atlantic (padd 1b)': {'new york', 'new jersey', 'pennsylvania', 'delaware', 'maryland', 'washington d.c.', 'virginia', 'west virginia'},
                'lower atlantic (padd 1c)': {'delaware', 'florida', 'georgia', 'maryland', 'north carolina', 'south carolina', 'virginia', 'west virginia', 'washington d.c'},
                'midwest (padd 2)': {'illinois', 'indiana', 'iowa', 'kansas', 'michigan', 'minnesota', 'missouri', 'nebraska', 'north dakota', 'ohio', 'south dakota', 'wisconsin'},
                'gulf coast (padd 3)': {'texas', 'louisiana', 'mississippi', 'alabama', 'florida'},
                'rocky mountain (padd 4)': {'colorado', 'idaho', 'montana', 'nevada', 'utah', 'wyoming', 'new mexico', 'arizona'},
                'west coast (padd 5)': {'california', 'oregon', 'washington'},
                'west coast less california': {'oregon', 'washington'}
                }

    for k1 in region_dict:
        for k2 in region_dict:
            if region_dict[k1] == region_dict[k2]:
                continue
            elif len(region_dict[k1]) < len(region_dict[k2]):
                region_dict[k2] -= region_dict[k1]
            else:
                region_dict[k1] -= region_dict[k2]
                
    return region_dict

def getStatePrices(prices):
    state_pice_dict = {}
    cols = get_schema()
    states_from_regions = get_states_from_region()
    with open("states.json", 'r') as fh:
        states = json.load(fh)

    for i in range(len(cols)):
        cols[i] = re.sub('-', ' ', cols[i]).lower()
        try:
            state_pice_dict[states[cols[i]]] = prices[i]
        except KeyError:
            try:
                for _state in states_from_regions[cols[i]]:
                    try:
                        if _state in cols:
                            continue
                        state_pice_dict[states[_state]] = prices[i]
                    except KeyError:
                        pass
            except:
                pass

    return state_pice_dict

def create_map():
    data = list()
    annual_data_list = getAnnualFuelPrices("regular")[3:] # no annual data before 1993

    for annual_data in annual_data_list: # date at index 0
        state_pice_dict = getStatePrices(annual_data)
        states = []
        prices = []

        for k,v in state_pice_dict.items():
            states.append(k)
            prices.append(v)

        data.append(dict(visible = False,
            type = 'choropleth', 
            locations = states, 
            locationmode = 'USA-states', 
            colorscale = 'Portland',
            z = prices,
            colorbar = {
                'title':'Prices in USD',
                'thickness': 75,
                'thicknessmode': 'pixels',
                'len': 0.8,
                'lenmode': 'fraction',
                'outlinewidth': 0
                }
            )
        )

    data[0]['visible'] = True # To display data in a particular step by default

    steps = []
    for i in range(len(data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(data)],
            label = annual_data_list[i][0]
        )
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
    active = 0,
    currentvalue = {"prefix": "Year: "},
    pad = {"t": 1},
    steps = steps
    )]

    layout = dict(sliders=sliders, geo ={'scope': 'usa'}, paper_bgcolor='#1F2833')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(title=f"End-of-year regular fuel prices",
    autosize=False,
    width=700,
    height=700,
    margin=go.layout.Margin(l=20, r=20, b=10, t=35, pad=0),
    font=dict(
        size=14,
        color="#add8e6"
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON
