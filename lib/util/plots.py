import matplotlib
from lib.util.ui import draw_candlesticks, display_in_kitty
from matplotlib.ticker import FuncFormatter
matplotlib.use('agg')
import matplotlib.pyplot as plt
import json
import websockets
from collections import deque
from datetime import datetime
import blessed

SYMBOL = "btcusdt"
INTERVAL = "1s"  # 1s, 1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, etc.
MAX_CANDLES = 60
UPDATE_EVERY = 1
CHART_WIDTH = 14
CHART_HEIGHT = 6

current_mode = 'chart'
terminal = blessed.Terminal()

candles = deque([None] * MAX_CANDLES, maxlen=MAX_CANDLES)
candle_dict = {}

WS_URL = f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_{INTERVAL}"

update_count = 0


async def connect_and_plot():
    global update_count, candle_dict
    
    # todo: add customization
    
    fig, ax = plt.subplots(figsize=(CHART_WIDTH, CHART_HEIGHT))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    
    async with websockets.connect(WS_URL) as ws:
        print(f"Connected to Binance WebSocket for {SYMBOL.upper()} @ {INTERVAL}")
        
        while True:
            try:
                msg = await ws.recv()
                data = json.loads(msg)
                
                kline = data['k']
                open_time = kline['t']
                candle_data = {
                    'time': datetime.fromtimestamp(open_time / 1000),
                    'open': float(kline['o']),
                    'high': float(kline['h']),
                    'low': float(kline['l']),
                    'close': float(kline['c']),
                    'volume': float(kline['v']),
                    'is_closed': kline['x']
                }
                
                if open_time in candle_dict:
                    idx = candle_dict[open_time]
                    candles[idx] = candle_data
                else:
                    candles.append(candle_data)
                    candle_dict[open_time] = len(candles) - 1
                    
                    if len(candle_dict) > MAX_CANDLES * 2:
                        candle_dict = {k: i for i, (k, _) in enumerate(
                            sorted(candle_dict.items())[-MAX_CANDLES:]
                        )}
                
                update_count += 1
                
                if len(candles) >= 2 and update_count >= UPDATE_EVERY:
                    update_count = 0
                    
                    ax.clear()
                    ax.set_facecolor('#16213e')
                    
                    candles_list = [c for c in candles if c is not None]
                    draw_candlesticks(ax, candles_list, offset=MAX_CANDLES - len(candles_list))
                    
                    current_price = candles_list[-1]['close']
                    price_change = current_price - candles_list[-1]['open']
                    change_pct = (price_change / candles_list[-1]['open']) * 100
                    change_symbol = '+' if price_change >= 0 else ''
                    
                    ax.set_title(
                        f'{SYMBOL.upper()} ({INTERVAL}) - ${current_price:,.2f} '
                        f'({change_symbol}{price_change:,.2f} / {change_symbol}{change_pct:.2f}%)',
                        fontsize=14, color='white'
                    )
                    ax.set_xlabel('Candles', color='white')
                    ax.set_ylabel('Price (USD)', color='white')
                    
                    ax.set_xlim(-1, MAX_CANDLES)
                    
                    all_highs = [c['high'] for c in candles_list]
                    all_lows = [c['low'] for c in candles_list]
                    min_price = min(all_lows)
                    max_price = max(all_highs)
                    price_range = max_price - min_price
                    padding = max(price_range * 0.1, 10)
                    ax.set_ylim(min_price - padding, max_price + padding)
                    
                    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
                    
                    ax.tick_params(colors='white')
                    ax.spines['bottom'].set_color('white')
                    ax.spines['top'].set_color('white')
                    ax.spines['left'].set_color('white')
                    ax.spines['right'].set_color('white')
                    ax.grid(True, alpha=0.3, color='gray')
                    
                    fig.tight_layout()
                    display_in_kitty(fig)
                    
            except websockets.ConnectionClosed:
                print("Connection closed, reconnecting...")
                break
            except KeyboardInterrupt:
                print("\nExiting...")
                plt.close(fig)
                return
            except Exception as e:
                print(f"Error: {e}")
                continue
    
    plt.close(fig)
