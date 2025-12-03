import blessed
import asyncio

terminal = blessed.Terminal()


async def input_handler():
    global current_mode, SYMBOL, INTERVAL
    
    # todo: improve controls
    
    with terminal.cbreak():
        while True:
            if terminal.kbhit(timeout=0.1):
                key = terminal.inkey(timeout=0)
                
                if key.is_sequence:
                    if key.name == 'KEY_F1':
                        current_mode = 'chart'
                        print(f"\n[Mode: Chart View]")
                    elif key.name == 'KEY_F2':
                        current_mode = 'symbol'
                        print(f"\n[Mode: Symbol Selection]")
                    elif key.name == 'KEY_F3':
                        current_mode = 'interval'
                        print(f"\n[Mode: Interval Selection]")
                    elif key.name == 'KEY_F4':
                        current_mode = 'settings'
                        print(f"\n[Mode: Settings]")
                    elif key.name == 'KEY_ESCAPE':
                        current_mode = 'chart'
                        print(f"\n[Back to Chart]")
                
                elif key == 'q':
                    print("\nQuitting...")
                    return
                
                elif current_mode == 'symbol' and key in '123456789':
                    symbols = ['btcusdt', 'ethusdt', 'bnbusdt', 'solusdt', 'xrpusdt', 'adausdt', 'dogeusdt']
                    idx = int(key) - 1
                    if idx < len(symbols):
                        SYMBOL = symbols[idx]
                        print(f"\n[Symbol changed to: {SYMBOL.upper()}]")
                        current_mode = 'chart'
                
                elif current_mode == 'interval' and key in '123456789':
                    intervals = ['1s', '1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']
                    idx = int(key) - 1
                    if idx < len(intervals):
                        INTERVAL = intervals[idx]
                        print(f"\n[Interval changed to: {INTERVAL}]")
                        current_mode = 'chart'
            
            await asyncio.sleep(0.05)
