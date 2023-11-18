import plotly.graph_objects as go
from datetime import datetime


def grafic_func(dfpl):
    # dfpl = data[2000:2100]
    # fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
    #                 open=dfpl['Heiken_Open'],
    #                 high=dfpl['Heiken_High'],
    #                 low=dfpl['Heiken_Low'],
    #                 close=dfpl['Heiken_Close']),
    #                     go.Scatter(x=dfpl.index, y=dfpl.EMA10, line=dict(color='red', width=1), name="EMA10"),
    #                     go.Scatter(x=dfpl.index, y=dfpl.EMA30, line=dict(color='blue', width=1), name="EMA30")])

    # fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
    #                 marker=dict(size=5, color="MediumPurple"),
    #                 name="Signal")
    # fig.show()

    # dfpl = data[100:2200]
    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                    open=dfpl['Open'],
                    high=dfpl['High'],
                    low=dfpl['Low'],
                    close=dfpl['Close']),
                        go.Scatter(x=dfpl.index, y=dfpl.EMA10, line=dict(color='red', width=1), name="EMA10"),
                        go.Scatter(x=dfpl.index, y=dfpl.EMA30, line=dict(color='blue', width=1), name="EMA30")])

    fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
                    marker=dict(size=5, color="MediumPurple"),
                    name="Signal")
    fig.show()