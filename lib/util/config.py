from collections import deque
import blessed
from colorama import Fore

class config:
    SYMBOL = str("btcusdt")
    INTERVAL = str("1s")  # 1s, 1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, etc.
    MAX_CANDLES = 60
    UPDATE_EVERY = 1
    CHART_WIDTH = 14
    CHART_HEIGHT = 6
    CHART_BG = str("#1a1a2e")
    CHART_FG = str("#16213e")
    CANDLE_GAIN_COLOR = str("#00ff88")
    CANDLE_FALL_COLOR = str("#ff4444")
    TEXT_GAIN_COLOR = Fore.GREEN
    TEXT_FALL_COLOR = Fore.RED

    current_mode = 'chart'
    terminal = blessed.Terminal()

    candles = deque([None] * MAX_CANDLES, maxlen=MAX_CANDLES)
    candle_dict = {}
    
    refresh_plot = False
