from lib.util.input import input_handler
from lib.util.plots import connect_and_plot
import asyncio
import os
from lib.util.main_menu import main_menu


async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    await main_menu()


if __name__ == "__main__":
    asyncio.run(main())

