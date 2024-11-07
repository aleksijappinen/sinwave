import curses
import time
import math
import sympy as sp

# ASCII brightness dictionary
ascii_brightness = {
    1: '.',  # Darkest
    0.9: '_',
    0.8: '`',
    0.7: "'",  
    0.6: '^',  # Pretty dark
    0.5: '~', 
    0.4: '-',
    0.3: '*',  # Mid bright
    0.2: '~',
    0.1: '"',
    0: '&',  # Pretty bright
    -0.1: ';',
    -0.2: '!',
    -0.3: '@',  # Brightest
    -0.4: '#',
    -0.5: '%',
    -0.6: '&',  # Pretty bright
    -0.7: '8', 
    -0.8: '$',
    -0.9: '*',
    -1: '#'  # Mid bright
}

def spf(x):
    return sp.sin(x)**3

def f(x):
    return math.sin(x)**3

def g(x,factor,const):
    return (f(x)+const)*factor

def slope(x):
    delta_x = 0.01
    y1 = f(x)
    y2 = f(x + delta_x)
    return (y2 - y1) / delta_x  # Approximate derivative

def wave_animation(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch non-blocking

    height, width = stdscr.getmaxyx()  # Get the terminal size

    x = sp.symbols('x', real=True)
    df = sp.diff(spf(x),x)
    zeros = sp.solve(df,x)

    max, min = zeros[0], zeros[0]

    print(height, width)

    # Get the largest zero and the smallest zero from zeros
    for i in range(0, len(zeros)):
        if spf(zeros[i]) > max:
            max = zeros[i]

    for i in range(0, len(zeros)):
        if spf(zeros[i]) < min:
            min = zeros[i]

    const = 1

    factor = ((height-1)/2)/f(max)

    # if f(min) < 0:
    #     factor = ((height-1)/2)/f(max)
    # else:
    #     factor = (height-1)/f(max)

    scale = (2 * sp.pi) / (width/2)

    print(f"{min=}, {g(max,factor,const)}")

    print("Df: ", df)
    print("Zeros: ", zeros)
    print("Factor: ", factor)
    print("Constant: ", const)
    print("Scale: ", scale)

    slopes = list()

    # Calculate max slope for normalization
    max_slope = 0
    for x in range(width - 1):
        current_slope = abs(slope(x * scale))
        if current_slope > max_slope:
            max_slope = current_slope

    while True:
        stdscr.clear()  # Clear the screen
        time_offset = time.time()  # Get time once per frame iteration

        for x in range(width-1):
            # Calculate the y value using sine function
            y = int(g(x*scale + time_offset, factor, const))

            # Calculate the slope at the current x position
            slope_value = slope(x * scale + time_offset)
            if max_slope != 0:
                slope_value /= max_slope  # Normalize to [-1, 1]

            slopes.append(slope_value)

            # Get the corresponding character based on slope
            char = ascii_brightness.get(round(slope_value, 1), ' ')
            
            y_rev = height - y - 1 # Reverse y to correlate with curses reversed terminal
            
            if 0 < x < width and 0 < y_rev < height:
                stdscr.addstr(y_rev, x, char) # Draw the character
            
        stdscr.refresh()  # Refresh the screen
        
        if stdscr.getch() != -1:  # Exit on any key press
            for number in range(0, 50, 5): 
                print(slopes[number]) 
            break

if __name__ == '__main__':
    curses.wrapper(wave_animation)