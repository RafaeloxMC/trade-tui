import asyncio
from lib.menus.plots import connect_and_plot
from lib.menus.orderbook import connect_orderbook, display_orderbook
from lib.util.input import input_handler
import sys
from lib.util.config import config
from lib.menus.settings import open_settings
from lib.util.clear import clear


async def main_menu():
    clear()
    config.current_mode = "menu"
    while True:
        print("Select mode:")
        print("1. Chart mode")
        print("2. Order Book mode")
        print("98. Settings")
        print("99. Exit")
        mode = input("Select mode: ")

        if mode == "1":
            print("Switching to chart mode!")
            await show_chart()
        elif mode == "2":
            print("Switching to order book mode!")
            await show_orderbook()
        elif mode == "98":
            open_settings()
        elif mode == "99":
            sys.exit(0)
        else:
            print("Mode not found!")


async def show_chart():
    clear()
    config.current_mode = "chart"
    while config.current_mode == "chart":
        try:
            await asyncio.gather(
                connect_and_plot(),
                input_handler(),
                return_exceptions=True
            )
        except Exception as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(5)


async def show_orderbook():
    clear()
    config.current_mode = "orderbook"
    while config.current_mode == "orderbook":
        try:
            await asyncio.gather(
                connect_orderbook(),
                display_orderbook(),
                input_handler(),
                return_exceptions=True
            )
        except Exception as e:
            print(f"Order book error: {e}")
            await asyncio.sleep(5)
