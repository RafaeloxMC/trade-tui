import blessed
import asyncio
from lib.util.config import config


_original_message = "Q -> Main Menu"
_current_message = _original_message


async def input_handler():
    global _current_message
    _current_message = _original_message
    with config.terminal.cbreak():
        while config.current_mode in ("chart", "symbol", "interval", "orderbook"):
            clear_eol = getattr(config.terminal, 'clear_eol', '')
            if config.terminal.kbhit(timeout=0.1):
                key = config.terminal.inkey(timeout=0)

                if key == 'q':
                    _current_message = "Quitting..."
                    print(f"{_current_message}{clear_eol}",
                          end="\r", flush=True)
                    config.current_mode = "menu"
                    return
            print(f"{_current_message}{clear_eol}",
                  end="\r", flush=True)
            await asyncio.sleep(0.05)


def set_current_message(message: str):
    global _current_message
    _current_message = message


def reset_current_message():
    global _current_message
    _current_message = _original_message
