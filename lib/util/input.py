import blessed
import asyncio
from lib.util.config import config

original_message = "Q -> Main Menu"
current_message = original_message


async def input_handler():
    global current_mode, INTERVAL, current_message
    
    with config.terminal.cbreak():
        while config.current_mode in ("chart", "symbol", "interval", "orderbook"):
            if config.terminal.kbhit(timeout=0.1):
                key = config.terminal.inkey(timeout=0)
                
                if key == 'q':
                    current_message = ("Quitting...")
                    print(current_message)
                    config.current_mode = "menu"
                    return
            clear_eol = getattr(config.terminal, 'clear_eol', '')
            print(f"{current_message}{clear_eol}", end="\r")
            await asyncio.sleep(0.05)
