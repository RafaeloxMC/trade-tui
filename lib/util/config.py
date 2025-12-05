from collections import deque
import blessed


class config:
    SYMBOL = str("btcusdt")
    INTERVAL = "1s"  # 1s, 1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, etc.
    MAX_CANDLES = 60
    UPDATE_EVERY = 1
    CHART_WIDTH = 14
    CHART_HEIGHT = 6
    CHART_BG = "#1a1a2e"
    CHART_FG = "#16213e"

    current_mode = 'chart'
    terminal = blessed.Terminal()

    candles = deque([None] * MAX_CANDLES, maxlen=MAX_CANDLES)
    candle_dict = {}
