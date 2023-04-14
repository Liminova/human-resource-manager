from frontend.gui import Login

import sys

def main_gui():
    window = Login()
    window.run()

if __name__ == "__main__":
    try:
        main_gui()
    except KeyboardInterrupt:
        sys.exit(0)
