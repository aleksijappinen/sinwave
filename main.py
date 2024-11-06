import curses
import time
import sympy as sp

# Define the ASCII brightness dictionary
ascii_brightness = {
    0.1: '+',
    0.09: '%',
    0.08: '#',
    0.07: '@',  # Brightest
    0.06: '&',
    0.05: '$',
    0.04: '*',
    0.03: '!',
    0.02: '=',
    0.01: '8',
    0.0: '*',  # Mid brightness
    -0.01: '8',
    -0.02: '=',
    -0.03: '$',
    -0.04: '&',
    -0.05: '*',
    -0.06: '!',
    -0.07: '.',  # Darkest
    -0.08: "'",
    -0.09: '`',
    -0.1: '_'  # Least bright
}

def f(x):
    return sp.sin(x)

def g(x,factor,const):
    return (f(x)+const)*factor

def h(x,factor):
    return f(x)*factor

def slope(x):
    delta_x = 0.01
    y1 = f(x)
    y2 = f(x + delta_x)
    return (y2 - y1) / delta_x  # Approximate derivative

def wave_animation(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch non-blocking
    stdscr.timeout(5)   # Refresh every 5 milliseconds

    height, width = stdscr.getmaxyx()  # Get the terminal size

    scale = (2 * sp.pi) / width

    print(height, width)

    x = sp.symbols('x')
    n = sp.symbols('n')

    df = sp.diff(f(x),x)

    zeros = sp.solve(df,x)

    x1 = zeros[0]
    x2 = zeros[1]

    if f(x1) > f(x2):
        gap = f(x1) - f(x2)
        factor = sp.solve(sp.Eq(h(x2,n), ((height-1)/2)))
        constant = sp.solve(sp.Eq(g(x2,factor[0],-n), -1))
    else:
        gap = f(x2) - f(x1)
        factor = sp.solve(sp.Eq(h(x2,n), ((height-1)/2)))
        constant = sp.solve(sp.Eq(g(x1,factor[0],-n), -1))

    factor = float(factor[0])
    constant = float(constant[0])

    print("Df: ", df)
    print("Zeros: ", zeros)
    print("Gap: ", gap)
    print("Factor: ", factor)
    print("Constant: ", constant)

    while True:
        stdscr.clear()  # Clear the screen
        time_offset = time.time()*5  # Get time once per frame iteration

        for x in range(width-1):
            # Calculate the y value using sine function
            y = int(g(x*scale + time_offset, factor, constant))

            # Calculate the slope at the current x position
            slope_value = slope(x + time_offset)

            # Get the corresponding character based on slope
            char = ascii_brightness.get(round(slope_value, 2), ' ')

            if 0 < x < width and 0 < y < height:
                stdscr.addstr(y, x, '*') # Draw the character at the calculated position

        stdscr.refresh()  # Refresh the screen
        if stdscr.getch() != -1:  # Exit on any key press
            break

if __name__ == '__main__':
    curses.wrapper(wave_animation)