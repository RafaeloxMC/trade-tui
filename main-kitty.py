from lib.menus.main_menu import main_menu
import asyncio
import os


async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    await main_menu()


if __name__ == "__main__":
    asyncio.run(main())
