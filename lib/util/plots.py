import matplotlib
from lib.util.ui import draw_candlesticks, display_in_kitty
from matplotlib.ticker import FuncFormatter
from lib.util.config import config
matplotlib.use('agg')
import matplotlib.pyplot as plt
import json
import websockets
from datetime import datetime

WS_URL = f"wss://stream.binance.com:9443/ws/{config.SYMBOL}@kline_{config.INTERVAL}"

update_count = 0


async def connect_and_plot():
    global update_count
    
    fig, ax = plt.subplots(figsize=(config.CHART_WIDTH, config.CHART_HEIGHT))
    fig.set_facecolor(config.CHART_BG)
    ax.set_facecolor(config.CHART_FG)
    
    async with websockets.connect(WS_URL) as ws:
        print(f"Connected to Binance WebSocket for {config.SYMBOL.upper()} @ {config.INTERVAL}")
        
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
                
                if open_time in config.candle_dict:
                    idx = config.candle_dict[open_time]
                    config.candles[idx] = candle_data
                else:
                    config.candles.append(candle_data)
                    config.candle_dict[open_time] = len(config.candles) - 1
                    
                    if len(config.candle_dict) > config.MAX_CANDLES * 2:
                        config.candle_dict = {k: i for i, (k, _) in enumerate(
                            sorted(config.candle_dict.items())[-config.MAX_CANDLES:]
                        )}
                
                update_count += 1
                
                if len(config.candles) >= 2 and update_count >= config.UPDATE_EVERY:
                    update_count = 0
                    
                    ax.clear()
                    ax.set_facecolor(config.CHART_FG)
                    
                    candles_list = [c for c in config.candles if c is not None]
                    draw_candlesticks(ax, candles_list, offset=config.MAX_CANDLES - len(candles_list))
                    
                    current_price = candles_list[-1]['close']
                    price_change = current_price - candles_list[-1]['open']
                    change_pct = (price_change / candles_list[-1]['open']) * 100
                    change_symbol = '+' if price_change >= 0 else ''
                    
                    ax.set_title(
                        f'{config.SYMBOL.upper()} ({config.INTERVAL}) - ${current_price:,.2f} '
                        f'({change_symbol}{price_change:,.2f} / {change_symbol}{change_pct:.2f}%)',
                        fontsize=14, color='white'
                    )
                    ax.set_xlabel('Candles', color='white')
                    ax.set_ylabel('Price (USD)', color='white')
                    
                    ax.set_xlim(-1, config.MAX_CANDLES)
                    
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
