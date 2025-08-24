"""Entry point for the beginner-friendly calculator app.

Runs the Tkinter GUI.
"""

from calculator.gui import CalculatorApp


def main() -> None:
    app = CalculatorApp()
    app.run()


if __name__ == "__main__":
    main()


