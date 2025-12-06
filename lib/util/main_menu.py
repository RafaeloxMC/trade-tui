import asyncio
from lib.util.plots import connect_and_plot
from lib.util.input import input_handler
import sys
from lib.util.config import config


async def main_menu():
    config.current_mode = "menu"
    while True:
        print("Select mode:")
        print("1. Chart mode")
        print("99. Exit")
        mode = input("Select mode: ")
        
        if mode == "1":
            print("Switching to chart mode!")
            await show_chart()
        elif mode == "99":
            sys.exit(0)
        else:
            print("Mode not found!")
    

async def show_chart():
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
