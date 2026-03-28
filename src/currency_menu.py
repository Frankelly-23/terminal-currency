import curses


class Menu:
    def __init__(self, content, colors, beginY, beginX) -> None:
        self.content = content
        self.colors = colors
        self.nlines = 5 
        self.ncols = len(self.content) + 6 
        self.beginY = beginY
        self.beginX = beginX
        
        self.menuscr = curses.newwin(self.nlines, self.ncols, beginY, beginX)
        self.height, self.width = self.menuscr.getmaxyx()
        self.contentX = max(0, (self.width - len(self.content)) // 2)
        self.contentY = self.height//2 

    def draw_menu(self):

        self.menuscr.erase()
        self.menuscr.box()

        self.menuscr.addstr(self.contentY, self.contentX, self.content, self.colors[0])
        self.menuscr.noutrefresh()


