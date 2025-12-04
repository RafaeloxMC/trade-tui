from matplotlib.patches import Rectangle
import base64
import io
import sys


def draw_candlesticks(ax, candles_list, offset=0):
    width = 0.6 
    
    for i, candle in enumerate(candles_list):
        x = i + offset
        open_price = candle['open']
        close_price = candle['close']
        high_price = candle['high']
        low_price = candle['low']
        
        # todo: add customizable colors
        
        if close_price >= open_price:
            color = '#00ff88'
            body_bottom = open_price
            body_height = close_price - open_price
        else:
            color = '#ff4444'
            body_bottom = close_price
            body_height = open_price - close_price
        
        ax.plot([x, x], [low_price, high_price], color=color, linewidth=1)
        
        if body_height == 0:
            body_height = 0.01
        rect = Rectangle((x - width / 2, body_bottom), width, body_height,
                         facecolor=color, edgecolor=color, linewidth=1)
        ax.add_patch(rect)


def display_in_kitty(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='#1a1a2e')
    buf.seek(0)
    data = base64.b64encode(buf.getvalue()).decode('ascii')
    
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.write(f'\033_Ga=T,f=100;{data}\033\\')
    sys.stdout.write('\n')
    sys.stdout.flush()
    buf.close()
