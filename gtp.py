import curses
import time
import sympy

def wave_animation(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(0)

    height, width = stdscr.getmaxyx()

    # Constants for scaling and wave speed
    wave_amplitude = height // 4
    wave_frequency = 0.1
    speed = 25

    while True:
        stdscr.clear()
        offset = time.time() * speed  # Update offset based on time for animation

        for x in range(width):
            y = int((sympy.sin(x * wave_frequency + offset) * wave_amplitude) + (height // 2))
            if 0 <= y < height:
                stdscr.addch(y, x, '*')

        stdscr.refresh()
        time.sleep(0.01)  # Delay to control frame rate

        if stdscr.getch() != -1:
            break

if __name__ == '__main__':
    curses.wrapper(wave_animation)
