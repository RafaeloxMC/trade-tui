import matplotlib
from lib.util.input import input_handler
from lib.util.plots import connect_and_plot
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Rectangle
import json
import asyncio
import websockets
from collections import deque
from datetime import datetime
import sys
import io
import base64
import blessed

SYMBOL = "btcusdt"
INTERVAL = "1s"  # 1s, 1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, ...
MAX_CANDLES = 60
UPDATE_EVERY = 1
CHART_WIDTH = 14
CHART_HEIGHT = 6

MODES = {
    'F1': 'chart',
    'F2': 'symbol',
    'F3': 'interval',
    'F4': 'settings',
}

current_mode = 'chart'
terminal = blessed.Terminal()

candles = deque(maxlen=MAX_CANDLES)
candle_dict = {}

WS_URL = f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_{INTERVAL}"

update_count = 0


async def main():
    while True:
        try:
            await asyncio.gather(
                connect_and_plot(),
                input_handler(),
                return_exceptions=True
            )
        except Exception as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())

