from lib.util.input import input_handler
from lib.util.plots import connect_and_plot
import asyncio


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

