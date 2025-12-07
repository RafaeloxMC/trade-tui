from lib.menus.main_menu import main_menu
from lib.util.config import config
import asyncio
import os


async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    config.load_from_file()
    await main_menu()


if __name__ == "__main__":
    asyncio.run(main())
