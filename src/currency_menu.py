import curses


class Menu:
    def __init__(self, content: str, colors: list[int]) -> None:
        self.content: str = content
        self.colors: list[int] = colors

    def make_menu_window(self, nlines, ncols, beginY, beginX):        

        self.menuscr: curses.window = curses.newwin(nlines, ncols, beginY, beginX)
        self.height, self.width = self.menuscr.getmaxyx()
        self.contentX: int = max(0, (self.width - len(self.content)) // 2)
        self.contentY: int = self.height//2 
        self.draw_menu()

    def draw_menu(self):
        self.menuscr.erase()
        self.menuscr.box()

        self.menuscr.addstr(self.contentY, self.contentX, self.content, self.colors[0])
        self.menuscr.noutrefresh()


