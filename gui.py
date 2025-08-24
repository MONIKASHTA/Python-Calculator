from __future__ import annotations

import tkinter as tk
from typing import Callable

from .logic import CalculatorEngine


class CalculatorApp:
    """Tkinter-based calculator GUI that delegates logic to CalculatorEngine."""

    def __init__(self) -> None:
        self.engine = CalculatorEngine()
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.resizable(False, False)

        self.display_var = tk.StringVar(value=self.engine.get_display())

        self._build_ui()
        self._bind_keys()

    # ---------- UI building ----------
    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, padx=8, pady=8)
        outer.grid(row=0, column=0)

        display = tk.Entry(
            outer,
            textvariable=self.display_var,
            justify="right",
            font=("Segoe UI", 20),
            state="readonly",
            readonlybackground="#ffffff",
            relief="flat",
            width=15,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 8))

        def add_btn(text: str, row: int, col: int, cmd: Callable[[], None], colspan: int = 1) -> None:
            btn = tk.Button(
                outer,
                text=text,
                command=cmd,
                width=4 * colspan,
                height=2,
                font=("Segoe UI", 12),
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky="nsew")

        # Row 1
        add_btn("AC", 1, 0, self._on_all_clear)
        add_btn("CE", 1, 1, self._on_clear_entry)
        add_btn("%", 1, 2, self._on_percent)
        add_btn("/", 1, 3, lambda: self._on_operator("/"))

        # Row 2
        add_btn("7", 2, 0, lambda: self._on_digit("7"))
        add_btn("8", 2, 1, lambda: self._on_digit("8"))
        add_btn("9", 2, 2, lambda: self._on_digit("9"))
        add_btn("*", 2, 3, lambda: self._on_operator("*"))

        # Row 3
        add_btn("4", 3, 0, lambda: self._on_digit("4"))
        add_btn("5", 3, 1, lambda: self._on_digit("5"))
        add_btn("6", 3, 2, lambda: self._on_digit("6"))
        add_btn("-", 3, 3, lambda: self._on_operator("-"))

        # Row 4
        add_btn("1", 4, 0, lambda: self._on_digit("1"))
        add_btn("2", 4, 1, lambda: self._on_digit("2"))
        add_btn("3", 4, 2, lambda: self._on_digit("3"))
        add_btn("+", 4, 3, lambda: self._on_operator("+"))

        # Row 5
        add_btn("±", 5, 0, self._on_toggle_sign)
        add_btn("0", 5, 1, lambda: self._on_digit("0"))
        add_btn(".", 5, 2, self._on_decimal)
        add_btn("=", 5, 3, self._on_equals)

        for r in range(6):
            outer.grid_rowconfigure(r, weight=1)
        for c in range(4):
            outer.grid_columnconfigure(c, weight=1)

    def _bind_keys(self) -> None:
        self.root.bind("<Key>", self._on_key)
        self.root.bind("<Return>", lambda e: self._refresh(self.engine.equals()))
        self.root.bind("<KP_Enter>", lambda e: self._refresh(self.engine.equals()))
        self.root.bind("<BackSpace>", lambda e: self._refresh(self.engine.clear_entry()))
        self.root.bind("<Escape>", lambda e: self._refresh(self.engine.all_clear()))

    # ---------- Event handlers ----------
    def _refresh(self, value: str) -> None:
        self.display_var.set(value)

    def _on_digit(self, digit: str) -> None:
        self._refresh(self.engine.input_digit(digit))

    def _on_decimal(self) -> None:
        self._refresh(self.engine.input_decimal())

    def _on_operator(self, op: str) -> None:
        self._refresh(self.engine.input_operator(op))

    def _on_equals(self) -> None:
        self._refresh(self.engine.equals())

    def _on_all_clear(self) -> None:
        self._refresh(self.engine.all_clear())

    def _on_clear_entry(self) -> None:
        self._refresh(self.engine.clear_entry())

    def _on_percent(self) -> None:
        self._refresh(self.engine.percent())

    def _on_toggle_sign(self) -> None:
        self._refresh(self.engine.toggle_sign())

    def _on_key(self, event: tk.Event) -> None:  # type: ignore[name-defined]
        ch = event.char
        if ch.isdigit():
            self._on_digit(ch)
            return
        if ch in "+-*/":
            self._on_operator(ch)
            return
        if ch == ".":
            self._on_decimal()
            return
        if ch in {"~", "_"}:  # layout-dependent shortcuts for sign toggle
            self._on_toggle_sign()

    # ---------- Lifecycle ----------
    def run(self) -> None:
        self.root.mainloop()


