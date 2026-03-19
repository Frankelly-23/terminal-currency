
import curses
from curses import wrapper
from currency_screen import Currencyscr 
from currency_menu import Menu
from config import Config
import requests

config = Config()

def get_Currencies():
    try:
        res = requests.get("https://api.frankfurter.app/latest")
        res.raise_for_status()
        data = res.json()
        rates = data["rates"] 

        continents = config.get_continents()

        result  = {}
        for continent, currency_map in continents.items():
            result[continent] = [[f"{name}: {rates[code]:.2f}", f"{code}", rates[code]] for name, code in currency_map.items() if code in rates]

        return result

    except Exception:
        return None


def draw_error(color, stdscr):
    stdscr.erase()
    stdscr.box()
    height, width = stdscr.getmaxyx()
    error_message = "We've had an issue getting the data :("
    exit_message = "Press any key to leave"
    
    mid_y, mid_x = height // 2, width // 2
    
    stdscr.addstr(mid_y, mid_x - len(error_message)//2, error_message, color[1])
    stdscr.addstr(mid_y + 2, mid_x - len(exit_message)//2, exit_message, color[0])
    
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    # colors
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) 
    MAGENTA = curses.color_pair(1)
    GREEN  = curses.color_pair(2)
    RED = curses.color_pair(3)
    
    currencies_per_continent = get_Currencies()

    if currencies_per_continent is None:
       draw_error([MAGENTA, RED], stdscr) 
       return

    curses.curs_set(0)  
    
    title = "World Currencies  🌍"
    asia_scr = Currencyscr(
            currencies_per_continent['asia'], 
            "Asia", 
            20, 30, 10, 10,
            [RED, MAGENTA, GREEN]
            ) 
    europe_scr = Currencyscr(
            currencies_per_continent['europe'], 
            "Europe", 
            20, 30, 10, 40, 
            [RED, MAGENTA, GREEN]
            ) 
    america_scr = Currencyscr(
        currencies_per_continent['america'] , 
            "America", 
            20, 30, 10, 70, 
            [RED, MAGENTA, GREEN])
    ocenia_and_africa_scr = Currencyscr(
            currencies_per_continent['oceania_africa'], 
            "Oceania & Africa", 
            20, 30, 10, 100, 
            [RED, MAGENTA, GREEN]) 

    menu_content =  "[+] c | Toggle chart view"
    exit_menu_content =  "[+] q | exit"
    toggle_chart_menu = Menu(menu_content, [MAGENTA, GREEN], 30, 10) 
    exit_menu = Menu(exit_menu_content, [RED, GREEN], 30, 40) 

    # If dynamic updates are added later.
    stdscr.timeout(-1)


    def draw_all(isChartMode):

        #Main Screen
        stdscr.erase()
        stdscr.box()
        height, width = stdscr.getmaxyx()
        XMESSAGE, YMESSAGE = abs((width // 2) - (len(title) // 2)), height // 7 
        stdscr.addstr(YMESSAGE, XMESSAGE, title, MAGENTA)
        stdscr.noutrefresh()

        if isChartMode:
            asia_scr.chart_mode()
            europe_scr.chart_mode()
            america_scr.chart_mode()
            ocenia_and_africa_scr.chart_mode()
        else:
            asia_scr.write_currency()
            europe_scr.write_currency()
            america_scr.write_currency()
            ocenia_and_africa_scr.write_currency()


        toggle_chart_menu.draw_menu()  
        exit_menu.draw_menu()
        
        curses.doupdate()

    chartMode = False 
    while True:
        draw_all(chartMode)
        # Check for user input (q to quit)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('c'):
            chartMode = not chartMode
        elif key == curses.KEY_RESIZE:
            draw_all(chartMode)

if __name__ == '__main__':
    wrapper(main)


