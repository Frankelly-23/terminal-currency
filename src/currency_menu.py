import curses


class Menu:
    def __init__(self, content: str, colors: list[int]) -> None:
        self.content: str = content
        self.colors: list[int] = colors
        self.nlines: int = 5 
        self.ncols: int = len(self.content) + 4 

    def make_menu_window(self, beginY, beginX):        
        self.menuscr: curses.window = curses.newwin(self.nlines, self.ncols, beginY, beginX) 
        self.height, self.width = self.menuscr.getmaxyx()
        self.contentX: int = max(0, (self.width - len(self.content)) // 2)
        self.contentY: int = self.height//2 

        self.draw_menu()

    def draw_menu(self):
        self.menuscr.erase()
        self.menuscr.box()

        self.menuscr.addstr(self.contentY, self.contentX, self.content, self.colors[0])
        self.menuscr.noutrefresh()


