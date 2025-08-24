## Python Calculator (Beginner-Friendly, with GUI)

This is a small, well-structured calculator app for beginners. It uses only the Python standard library (`tkinter`) and follows best practices by separating calculation logic from the user interface.

If you are new to Python, this project is a gentle way to learn how a program is organized and how a GUI (Graphical User Interface) talks to the logic.

### Features
- Basic operations: add, subtract, multiply, divide
- Percent, sign toggle (+/−), decimal input, clear entry (CE) and all clear (AC)
- Keyboard input for digits, operators, Enter (=), Backspace (CE), and Escape (AC)

### Requirements
- Python 3.9+
- No external dependencies

### Install Python (Windows)
- Download and install Python from the official site: [Download Python](https://www.python.org/downloads/)
- During installation, check “Add Python to PATH”.
- Verify installation in a new terminal:
  ```bash
  python --version
  ```
  It should print something like `Python 3.11.x`.

### Run
```bash
python main.py
```

If `python` maps to Python 2 on your system, use:
```bash
python3 main.py
```

You should see a window titled “Calculator”. Click buttons with your mouse or use the keyboard.

### Project Structure
```
python-calculator/
├─ calculator/
│  ├─ __init__.py
│  ├─ gui.py         # Tkinter UI (View/Controller)
│  └─ logic.py       # Calculation engine (Model)
└─ main.py           # Entry point
```

### How it works (Code Flow)
The app is intentionally split into two parts so beginners can focus on one thing at a time:

- `calculator/logic.py` contains `CalculatorEngine`, a small state machine that knows how to:
  - Accept inputs (digits, decimal point, operators)
  - Track a stored value, a pending operator, and the current display
  - Compute results and handle edge cases (e.g., divide by zero shows `Error`)

- `calculator/gui.py` contains `CalculatorApp` (Tkinter).
  - It renders the display and buttons, wires button and keyboard events to the engine, and refreshes the display when the engine changes.

High-level flow:
1. User presses a button or key.
2. The GUI calls a corresponding method on `CalculatorEngine`.
3. `CalculatorEngine` updates its internal state and returns the new display value.
4. The GUI updates the on-screen display.

Example: typing `1`, `2`, `+`, `3`, `=`
- `1` → engine sets display to `1`
- `2` → engine appends → `12`
- `+` → engine remembers `12` as the stored value, sets pending operator to `+`, marks “just evaluated” so the next digit starts fresh
- `3` → engine starts a new number → `3`
- `=` → engine applies `stored_value (12) + current (3)` → display becomes `15`

### Keyboard Shortcuts
- **Digits**: `0-9`
- **Operators**: `+ - * /`
- **Decimal point**: `.`
- **Equals**: `Enter` (or keypad Enter)
- **Clear entry**: `Backspace` (removes last character)
- **All clear**: `Esc` (resets everything)
- **Sign toggle**: `~` or `_` (varies by keyboard layout)

Tip: You can mix keyboard and mouse. For example, type numbers on the keyboard and click operators with the mouse.

### What happens when you press a button?
- **Digits** call `CalculatorEngine.input_digit(d)`. The engine builds the current number, handling leading zeros and fresh starts after `=`.
- **. (decimal)** calls `CalculatorEngine.input_decimal()`. The engine ensures only one decimal point exists.
- **+/−** calls `CalculatorEngine.toggle_sign()`. It flips the sign unless the number is `0`.
- **% (percent)** calls `CalculatorEngine.percent()`. It divides the current number by 100.
- **+  −  ×  ÷** call `CalculatorEngine.input_operator(op)`. The engine stores the current number and operator, and prepares for the next number.
- **=** calls `CalculatorEngine.equals()`. The engine performs the pending operation and shows the result.
- **CE** calls `CalculatorEngine.clear_entry()`. It acts like backspace for the current number.
- **AC** calls `CalculatorEngine.all_clear()`. It resets everything.

Edge cases handled for you:
- Divide by zero shows `Error`. Typing a digit after that starts fresh.
- After pressing `=`, the next digit starts a new number (doesn’t append to the result).

### Notes for Beginners
- **Read code in this order**: start with `main.py`, then `calculator/gui.py`, then `calculator/logic.py`.
- **Single responsibility**: The GUI never does math; it only displays and forwards actions. The engine never draws UI; it only computes.
- **Type hints**: Functions have return types (e.g., `-> str`) to make code easier to understand.

### Customize the app (easy exercises)
- Add a button for square (`x²`) or square root and implement it in the engine.
- Change fonts or colors in `calculator/gui.py`.
- Add a memory feature (M+, M-, MR, MC) by extending `CalculatorState` and the engine.
- Add a small “history” label that shows the last operation.

### Troubleshooting
- The window doesn’t appear: ensure you installed Python from the official site and are running `python main.py` from the project folder.
- Import error for `tkinter`: on Windows and macOS, `tkinter` ships with the official Python installer. If missing, reinstall Python from the official source.
- Garbled characters or unexpected keys: try clicking the buttons instead; keyboard layouts differ.

### What is `__pycache__`?
- Python creates a `__pycache__` folder to store compiled bytecode (`*.pyc`) so modules import faster.
- It is safe to delete; Python will recreate it automatically next time you run the program.

### License
MIT
