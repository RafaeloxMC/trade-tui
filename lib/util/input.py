import blessed
import asyncio
from lib.util.config import config

original_message = "F1 > Chart View; F2 > Symbol Selection; F3 > Interval Selection; Q > Main Menu"
current_message = original_message


async def input_handler():
    global current_mode, INTERVAL, current_message
    
    # todo: improve controls
    
    with config.terminal.cbreak():
        while config.current_mode in ("chart", "symbol", "interval"):
            if config.terminal.kbhit(timeout=0.1):
                key = config.terminal.inkey(timeout=0)
                
                if key.is_sequence:
                    if key.name == 'KEY_F1':
                        current_mode = 'chart'
                        current_message = (f"[Mode: Chart View]")
                    elif key.name == 'KEY_F2':
                        current_mode = 'symbol'
                        current_message = (f"[Mode: Symbol Selection]")
                    elif key.name == 'KEY_F3':
                        current_mode = 'interval'
                        current_message = (f"[Mode: Interval Selection]")
                
                elif key == 'q':
                    current_message = ("Quitting...")
                    print(current_message)
                    config.current_mode = "menu"
                    return
                
                elif current_mode == 'symbol' and key in '123456789':
                    symbols = ['btcusdt', 'ethusdt', 'bnbusdt', 'solusdt', 'xrpusdt', 'adausdt', 'dogeusdt']
                    idx = int(key) - 1
                    if idx < len(symbols):
                        SYMBOL = symbols[idx]
                        config.SYMBOL = SYMBOL
                        current_message = (f"[Symbol changed to: {SYMBOL.upper()}]")
                        current_mode = 'chart'
                        config.candle_dict.clear()
                        config.candles.clear()
                        config.refresh_plot = True
                
                elif current_mode == 'interval' and key in '123456789':
                    intervals = ['1s', '1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']
                    idx = int(key) - 1
                    if idx < len(intervals):
                        INTERVAL = intervals[idx]
                        config.INTERVAL = INTERVAL
                        current_message = (f"[Interval changed to: {INTERVAL}]")
                        current_mode = 'chart'
                        config.candle_dict.clear()
                        config.candles.clear()
                        config.refresh_plot = True
            clear_eol = getattr(config.terminal, 'clear_eol', '')
            print(f"{current_message}{clear_eol}", end="\r")
            await asyncio.sleep(0.05)
