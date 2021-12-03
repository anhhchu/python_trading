import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import kaleido

### Reference: https://www.alpharithms.com/calculate-macd-python-272222/ ***
        

def draw_candlestick_MA(ticker, df, shorter_window, longer_window, is_static=False):
    # Calculate and define moving average of window1 periods
    avg1 = df.Close.rolling(window=shorter_window, min_periods=1).mean()

    # Calculate and define moving average of window2 periods
    avg2 = df.Close.rolling(window=longer_window, min_periods=1).mean()
        
    
    # Construct a 2 x 1 Plotly figure
    fig = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": True}], [{"secondary_y": False}]])
    
    # Add Volume
    fig.add_trace(
        go.Bar(x=df.index, y=df.Volume,
                       name='Volume', opacity=0.8), row=1, col=1, secondary_y=True
    )
    
    # Candlestick chart for pricing
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name=ticker,
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            showlegend=False
        ), row=1, col=1, secondary_y=False,
    )
    
    # Moving Average line chart
    fig.add_trace(
        go.Scatter(x=df.index, y=avg1, name=f'MA{shorter_window}'),secondary_y=False)
    fig.add_trace(
          go.Scatter(x=df.index, y=avg2, name=f'MA{longer_window}'),secondary_y=False)
        
    # Fast Signal (%k)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['MACD_12_26_9'],
            line=dict(color='#ff9900', width=2),
            name='macd',
            showlegend=True,
            legendgroup='2',
        ), row=2, col=1
    )
    # Slow signal (%d)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['MACDs_12_26_9'],
            line=dict(color='#000000', width=2),
            # showlegend=False,
            legendgroup='2',
            name='signal'
        ), row=2, col=1
    )
    # Colorize the histogram values
    colors = np.where(df['MACDh_12_26_9'] < 0, '#000', '#ff9900')
    # Plot the histogram
    fig.append_trace(
        go.Bar(
            x=df.index,
            y=df['MACDh_12_26_9'],
            name='histogram',
            marker_color=colors,
        ), row=2, col=1
    )
    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        width=1000,
        height=800,
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=15,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        ),
        legend=dict( orientation='h',yanchor='middle', y=1.1, xanchor="left", x=0.5),
        hovermode='x',
        hoverlabel=dict(font=dict(size=10))
    )
    # Update options and show plot
    fig.update_layout(layout)
    if not is_static:
        fig.show()
    else:
        fig.show(renderer="png")
        
        
def draw_patterns(df, shorter_window, longer_window, patterns, is_static=False):
    # Calculate and define moving average of window1 periods
    avg1 = df.Close.rolling(window=shorter_window, min_periods=1).mean()

    # Calculate and define moving average of window2 periods
    avg2 = df.Close.rolling(window=longer_window, min_periods=1).mean()
        
    
    # Construct a 2 x 1 Plotly figure
    fig = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": True}], [{"secondary_y": False}]])
    
    # Add Event
    
    for pattern in patterns:
        colors = np.where(df[pattern] < 0, '#a84a32', '#278c5b')
        fig.add_trace(
                go.Scatter(mode='markers',x=df.index, y=df[pattern], name=pattern,
                           marker=dict(symbol='star-diamond', size=10, opacity=0.5),
                           marker_color=colors
                          ), row=1, col=1, secondary_y=True, 
        )
    # Candlestick chart for pricing
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='price',
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            showlegend=False
        ), row=1, col=1, secondary_y=False,
    )
    
    # Moving Average line chart
    fig.add_trace(
        go.Scatter(x=df.index, y=avg1, name=f'MA{shorter_window}'),secondary_y=False)
    fig.add_trace(
          go.Scatter(x=df.index, y=avg2, name=f'MA{longer_window}'),secondary_y=False)
        
    # Fast Signal (%k)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['MACD_12_26_9'],
            line=dict(color='#ff9900', width=2),
            name='macd',
            showlegend=True,
            legendgroup='2',
        ), row=2, col=1
    )
    # Slow signal (%d)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['MACDs_12_26_9'],
            line=dict(color='#000000', width=2),
            # showlegend=False,
            legendgroup='2',
            name='signal'
        ), row=2, col=1
    )
    # Colorize the histogram values
    colors = np.where(df['MACDh_12_26_9'] < 0, '#000', '#ff9900')
    # Plot the histogram
    fig.append_trace(
        go.Bar(
            x=df.index,
            y=df['MACDh_12_26_9'],
            name='histogram',
            marker_color=colors,
        ), row=2, col=1
    )
    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        width=1000,
        height=800,
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=15,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        ),
        #legend=dict( orientation='h',yanchor='bottom', y=0, xanchor="left", x=0.5, font_size = 10),
        legend=dict(font_size=10),
        hovermode='x',
        hoverlabel=dict(font=dict(size=10))
    )
    # Update options and show plot
    fig.update_layout(layout)
    fig['layout']['yaxis2']['showgrid'] = False
    # Set y-axes titles
    if not is_static:
        fig.show()
    else:
        fig.show(renderer="png")
        
        


        
        

