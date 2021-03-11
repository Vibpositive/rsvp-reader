# import newgui
# from com.vibpositive.gui.gui import Gui
import com.vibpositive.gui.gui as gui

def main():
    g = gui.MainGui()
    try:
        g.master.mainloop()
    finally:
        pass


if __name__ == '__main__':
    main()
