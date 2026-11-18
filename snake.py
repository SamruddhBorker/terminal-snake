#!/usr/bin/env python3
"""terminal-snake: classic Snake in your terminal. Standard library only.

Controls: arrow keys or WASD to steer, Q to quit.
Works on Windows (msvcrt) and macOS/Linux (curses).
"""
from __future__ import annotations

import random
import sys
import time
from dataclasses import dataclass, field

WIDTH, HEIGHT = 30, 15
DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}


@dataclass
class Game:
    width: int = WIDTH
    height: int = HEIGHT
    rng: random.Random = field(default_factory=random.Random)
    snake: list[tuple[int, int]] = field(default_factory=list)
    direction: str = "right"
    food: tuple[int, int] = (0, 0)
    score: int = 0
    alive: bool = True

    def __post_init__(self) -> None:
        cx, cy = self.width // 2, self.height // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]  # head first
        self.food = self._place_food()

    def _place_food(self) -> tuple[int, int]:
        free = [(x, y) for x in range(self.width) for y in range(self.height)
                if (x, y) not in self.snake]
        return self.rng.choice(free) if free else (-1, -1)

    def turn(self, new_dir: str) -> None:
        if new_dir in DIRS and new_dir != OPPOSITE[self.direction]:
            self.direction = new_dir

    def step(self) -> None:
        if not self.alive:
            return
        dx, dy = DIRS[self.direction]
        hx, hy = self.snake[0]
        head = (hx + dx, hy + dy)
        growing = head == self.food
        body = self.snake if growing else self.snake[:-1]  # tail moves away
        if not (0 <= head[0] < self.width and 0 <= head[1] < self.height) \
                or head in body:
            self.alive = False
            return
        self.snake.insert(0, head)
        if growing:
            self.score += 1
            self.food = self._place_food()
            if self.food == (-1, -1):  # board full: you win
                self.alive = False
        else:
            self.snake.pop()

    def render(self) -> str:
        top = "+" + "-" * self.width + "+"
        rows = [top]
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                p = (x, y)
                line += ("@" if p == self.snake[0] else
                         "o" if p in self.snake else
                         "*" if p == self.food else " ")
            rows.append("|" + line + "|")
        rows.append(top)
        rows.append(f" Score: {self.score}   (arrows/WASD, Q quits)")
        return "\n".join(rows)


KEYMAP = {"w": "up", "s": "down", "a": "left", "d": "right"}


def run_windows() -> int:
    import msvcrt
    import os
    # Constant empty string, no user input: the known trick that switches on
    # ANSI escape handling in the Windows console. Not an injection risk.
    os.system("")
    g = Game()
    print("\x1b[2J\x1b[?25l", end="")
    try:
        while g.alive:
            deadline = time.time() + max(0.06, 0.15 - g.score * 0.003)
            while time.time() < deadline:
                if msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    if ch in ("\x00", "\xe0"):  # arrow keys
                        ch = {"H": "w", "P": "s", "K": "a", "M": "d"}.get(
                            msvcrt.getwch(), "")
                    if ch.lower() == "q":
                        return 0
                    if ch.lower() in KEYMAP:
                        g.turn(KEYMAP[ch.lower()])
                time.sleep(0.005)
            g.step()
            print("\x1b[H" + g.render(), end="", flush=True)
    finally:
        print("\x1b[?25h")
    print(f"\nGame over! Final score: {g.score}")
    return 0


def run_curses() -> int:
    import curses

    def loop(stdscr) -> int:
        curses.curs_set(0)
        stdscr.nodelay(True)
        g = Game()
        keys = {curses.KEY_UP: "up", curses.KEY_DOWN: "down",
                curses.KEY_LEFT: "left", curses.KEY_RIGHT: "right"}
        while g.alive:
            deadline = time.time() + max(0.06, 0.15 - g.score * 0.003)
            while time.time() < deadline:
                k = stdscr.getch()
                if k in (ord("q"), ord("Q")):
                    return g.score
                if k in keys:
                    g.turn(keys[k])
                elif 0 <= k < 256 and chr(k).lower() in KEYMAP:
                    g.turn(KEYMAP[chr(k).lower()])
                time.sleep(0.005)
            g.step()
            stdscr.erase()
            for i, line in enumerate(g.render().split("\n")):
                stdscr.addstr(i, 0, line)
            stdscr.refresh()
        return g.score

    score = curses.wrapper(loop)
    print(f"Game over! Final score: {score}")
    return 0


def main() -> int:
    return run_windows() if sys.platform == "win32" else run_curses()


if __name__ == "__main__":
    sys.exit(main())
