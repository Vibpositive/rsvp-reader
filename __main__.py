import com.vibpositive.gui.gui as gui
import logging
import logging.config

logging.config.fileConfig('com/vibpositive/config/logging.conf')


def main():
    logger = logging.getLogger('file')
    g = gui.MainGui(logger)
    try:
        g.master.mainloop()
    finally:
        pass


if __name__ == '__main__':
    main()
