import curses
from currency_screen import Currencyscr 
import requests
from curses import wrapper

# data example 
# data = {
#   "amount": 1,
#   "base": "EUR",
#   "date": "2026-03-06",
#   "rates": {
#     "AUD": 1.6501,
#     "BRL": 6.1002,
#     "CAD": 1.5782,
#     "CHF": 0.9045,
#     "CNY": 7.9825,
#     "CZK": 24.419,
#     "DKK": 7.4708,
#     "GBP": 0.86693,
#     "HKD": 9.04,
#     "HUF": 393.4,
#     "IDR": 19623,
#     "ILS": 3.5756,
#     "INR": 106.17,
#     "ISK": 144.9,
#     "JPY": 182.57,
#     "KRW": 1717.02,
#     "MXN": 20.562,
#     "MYR": 4.562,
#     "NOK": 11.1725,
#     "NZD": 1.9687,
#     "PHP": 68.525,
#     "PLN": 4.2875,
#     "RON": 5.0951,
#     "SEK": 10.693,
#     "SGD": 1.481,
#     "THB": 36.966,
#     "TRY": 50.954,
#     "USD": 1.1561,
#     "ZAR": 19.3277
#   }
# }

  # ┃  - CNY - China
  # ┃  - HKD - Hong Kong    
  # ┃  - IDR - Indonesia
  # ┃  - INR - India  
  # ┃  - JPY - Japan  
  # ┃  - KRW - South Korea
  # ┃  - MYR - Malaysia
  # ┃  - PHP - Philippines  
  # ┃  - SGD - Singapore
  # ┃  - THB - Thailand

def get_Currencies() -> dict[str, list[str]] | str:
    try:
        res = requests.get("https://api.frankfurter.app/latest")
        data = res.json()
        rates = data["rates"] 

        continents = {
            "asia": {
                "Hong Kong": "HKD", "China": "CNY", "Indonesia": "IDR", "India": "INR", 
                "Japan": "JPY", "South Korea": "KRW", "Malaysia": "MYR", 
                "Philippines": "PHP", "Singapore": "SGD", "Thailand": "THB",
                "Israel": "ILS"
            },
            "europe": {
                "Switzerland": "CHF", "Czech Republic": "CZK", "Denmark": "DKK", 
                "United Kingdom": "GBP", "Hungary": "HUF", "Iceland": "ISK", 
                "Norway": "NOK", "Poland": "PLN", "Romania": "RON", 
                "Sweden": "SEK", "Turkey": "TRY"
            },
            "america": {
                "Canada": "CAD", "Mexico": "MXN", "United States": "USD", "Brazil": "BRL"
            },
            "oceania_africa": {
                "Australia": "AUD", "New Zealand": "NZD", "South Africa": "ZAR"

                }
        }

        result: dict[str, list[str]]  = {}
        for continent, currency_map in continents.items():
            result[continent] = [f"{name}: {rates[code]}" for name, code in currency_map.items()]

        return result

    except Exception:
        return "error"


def main(stdscr: curses.window):
    currencies_per_continent = get_Currencies()
    if currencies_per_continent == "error":
        print("Error")
        return
    curses.curs_set(0)  
    
    # colors
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) 
    MAGENTA = curses.color_pair(1)
    GREEN = curses.color_pair(2)
    # RED = curses.color_pair(3)
    
    message: str = "World Currencies  🌍"
    asia_scr = Currencyscr(currencies_per_continent['asia'], "Asia", 20, 30, 10, 10, GREEN) 
    europe_scr = Currencyscr(currencies_per_continent['europe'], "Europe", 20, 30, 10, 40, GREEN) 
    america_scr = Currencyscr(currencies_per_continent['america'], "America", 20, 30, 10, 70, GREEN) 
    ocenia_and_africa_scr = Currencyscr(currencies_per_continent['oceania_africa'], "Oceania & Africa", 20, 30, 10, 100, GREEN) 
    
    # If dynamic updates are added later.
    stdscr.timeout(-1)
    
    def draw_all():
        #Main Screen
        stdscr.erase()
        stdscr.box()
        height, width = stdscr.getmaxyx()
        XMESSAGE, YMESSAGE = abs((width // 2) - (len(message) // 2)), height // 7 
        stdscr.addstr(YMESSAGE, XMESSAGE, message, MAGENTA)
        
        stdscr.noutrefresh()
        
        asia_scr.write_currency()
        europe_scr.write_currency()
        america_scr.write_currency()
        ocenia_and_africa_scr.write_currency()
        
        curses.doupdate()

    draw_all()
    
    while True:
        # Check for user input (q to quit)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_RESIZE:
            draw_all()


if __name__ == '__main__':
    wrapper(main)


