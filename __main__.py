import newgui


def main():
    g = newgui.NewGui()
    try:
        g.master.mainloop()
    finally:
        pass


if __name__ == '__main__':
    main()
