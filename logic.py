from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CalculatorState:
    current_display: str = "0"
    stored_value: Optional[float] = None
    pending_operator: Optional[str] = None
    just_evaluated: bool = False


class CalculatorEngine:
    """A simple four-function calculator state machine.

    Responsibilities:
    - Maintain the display string
    - Track a stored value and a pending operator
    - Perform calculations on demand
    """

    def __init__(self) -> None:
        self.state = CalculatorState()

    # ---------- Display helpers ----------
    def _set_display(self, value: str) -> str:
        self.state.current_display = value
        return self.state.current_display

    def _is_display_numeric(self) -> bool:
        try:
            float(self.state.current_display)
            return True
        except ValueError:
            return False

    def _format_number(self, value: float) -> str:
        # Avoid showing trailing .0 for integers
        if value == int(value):
            return str(int(value))
        # Limit to reasonable precision for display
        return ("%.*f" % (12, value)).rstrip("0").rstrip(".")

    def _display_to_number(self) -> Optional[float]:
        try:
            return float(self.state.current_display)
        except ValueError:
            return None

    def _clear_all_internal(self) -> None:
        self.state = CalculatorState()

    # ---------- Public API (called by GUI) ----------
    def get_display(self) -> str:
        return self.state.current_display

    def input_digit(self, digit: str) -> str:
        if digit not in "0123456789":
            return self.get_display()

        if self.state.just_evaluated:
            # Start fresh after equals
            self.state.just_evaluated = False
            self.state.current_display = "0"

        if not self._is_display_numeric():
            # Reset from error state
            return self._set_display(digit if digit != "0" else "0")

        if self.state.current_display in {"0", "-0"}:
            # Replace leading zero
            if self.state.current_display.startswith("-"):
                return self._set_display("-" + digit)
            return self._set_display(digit)

        return self._set_display(self.state.current_display + digit)

    def input_decimal(self) -> str:
        if self.state.just_evaluated:
            self.state.just_evaluated = False
            return self._set_display("0.")

        if not self._is_display_numeric():
            return self._set_display("0.")

        if "." not in self.state.current_display:
            return self._set_display(self.state.current_display + ".")
        return self.get_display()

    def toggle_sign(self) -> str:
        if self.state.current_display.startswith("-"):
            return self._set_display(self.state.current_display[1:])
        if self.state.current_display != "0":
            return self._set_display("-" + self.state.current_display)
        return self.get_display()

    def percent(self) -> str:
        number = self._display_to_number()
        if number is None:
            return self.get_display()
        return self._set_display(self._format_number(number / 100.0))

    def clear_entry(self) -> str:
        # Backspace one character; keep a single zero
        if self.state.just_evaluated:
            return self.all_clear()
        if not self._is_display_numeric():
            return self.all_clear()
        text = self.state.current_display
        if len(text) <= 1 or (len(text) == 2 and text.startswith("-")):
            return self._set_display("0")
        return self._set_display(text[:-1])

    def all_clear(self) -> str:
        self._clear_all_internal()
        return self.get_display()

    def _apply_pending(self, rhs: float) -> Optional[float]:
        if self.state.stored_value is None or self.state.pending_operator is None:
            return rhs
        op = self.state.pending_operator
        lhs = self.state.stored_value
        try:
            if op == "+":
                return lhs + rhs
            if op == "-":
                return lhs - rhs
            if op == "*":
                return lhs * rhs
            if op == "/":
                return lhs / rhs
        except ZeroDivisionError:
            return None
        return rhs

    def _set_error(self) -> str:
        self._clear_all_internal()
        return self._set_display("Error")

    def input_operator(self, operator: str) -> str:
        if operator not in {"+", "-", "*", "/"}:
            return self.get_display()

        number = self._display_to_number()
        if number is None:
            return self.get_display()

        if self.state.stored_value is None:
            self.state.stored_value = number
        else:
            result = self._apply_pending(number)
            if result is None:
                return self._set_error()
            self.state.stored_value = result

        self.state.pending_operator = operator
        self.state.current_display = self._format_number(self.state.stored_value)
        self.state.just_evaluated = True
        return self.get_display()

    def equals(self) -> str:
        number = self._display_to_number()
        if number is None:
            return self.get_display()

        result = self._apply_pending(number)
        if result is None:
            return self._set_error()

        formatted = self._format_number(result)
        self.state.current_display = formatted
        self.state.stored_value = None
        self.state.pending_operator = None
        self.state.just_evaluated = True
        return self.get_display()


