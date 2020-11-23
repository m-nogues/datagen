import os

import plotly.express as px
import pandas as pd


def report(json):
    df = pd.DataFrame([json])

def load(file):
    # Gets the name of the directory where the indicators are
    name = '.'.join(os.path.basename(file).split(".")[0:-1])

    if not os.path.exists(name + '/pdfs'):
        os.makedirs(name + '/pdfs')

    df = pd.DataFrame(dict(
        r=[1, 5, 2, 2, 3],
        theta=['processing cost','mechanical properties','chemical stability',
               'thermal stability', 'device integration']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')
    fig.show()