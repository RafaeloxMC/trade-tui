from lib.util.config import config
from colorama import Fore

def open_settings():
    print("===================== SETTINGS =====================")
    print("Which setting would you like to change?")
    print("---------------------- CHARTS ----------------------")
    print(f"1. SYMBOL ({config.SYMBOL})")
    print(f"2. INTERVAL ({config.INTERVAL})")
    print("---------------------- COLORS ----------------------")
    print(f"11. CANDLE COLORS ({config.CANDLE_GAIN_COLOR} / {config.CANDLE_FALL_COLOR})")
    print(f"12. CHART COLORS ({config.CHART_BG} / {config.CHART_FG})")
    print(f"13. TEXT COLOR GAIN ({config.TEXT_GAIN_COLOR}+$100{Fore.RESET})")
    print(f"14. TEXT COLOR FALL ({config.TEXT_FALL_COLOR}-$100{Fore.RESET})")
    print("----------------------- BACK -----------------------")
    print("99. Back")
    
    setting = input("[num] >")