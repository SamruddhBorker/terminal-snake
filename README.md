# terminal-snake

Classic Snake in your terminal. Pure Python standard library, no installs.

```bash
python snake.py
```

- Arrow keys or WASD to steer, `Q` to quit
- The game speeds up as your score grows
- Windows uses `msvcrt`; macOS/Linux use `curses`
- Game logic (`Game` class) is separate from rendering, so it's unit-tested

## Tests

```bash
python -m unittest -v
```

## License

MIT
