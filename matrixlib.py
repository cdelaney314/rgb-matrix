import RPi.GPIO as GPIO
import threading
import time
import font
import math

#FRAMES_PER_SECOND = 30
delay = 0.0001
class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

# some example colors
black = Color(0,0,0)
pure_red = Color(255,0,0)
pure_green = Color(0,255,0)
pure_blue = Color(0,0,255)
navy = Color(0,0,128)
maroon = Color(128,0,0)
yellow = Color(255,255,0)
cyan = Color(0,255,255)
pink = Color(255,0,255)
gray = Color(128,128,128)
white = Color(255,255,255)
purple = Color(102,0,204)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
red1_pin = 17
green1_pin = 18
blue1_pin = 22
red2_pin = 23
green2_pin = 24
blue2_pin = 25
clock_pin = 3
a_pin = 7
b_pin = 8
c_pin = 9
latch_pin = 4
oe_pin = 2

GPIO.setup(red1_pin, GPIO.OUT)
GPIO.setup(green1_pin, GPIO.OUT)
GPIO.setup(blue1_pin, GPIO.OUT)
GPIO.setup(red2_pin, GPIO.OUT)
GPIO.setup(green2_pin, GPIO.OUT)
GPIO.setup(blue2_pin, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(a_pin, GPIO.OUT)
GPIO.setup(b_pin, GPIO.OUT)
GPIO.setup(c_pin, GPIO.OUT)
GPIO.setup(latch_pin, GPIO.OUT)
GPIO.setup(oe_pin, GPIO.OUT)

screen = [[black for x in range(32)] for y in range(16)]

def clock():
    GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)

def latch():
    GPIO.output(latch_pin, 1)
    GPIO.output(latch_pin, 0)

def bits_from_int(x):
    c_bit = x & 4
    b_bit = x & 2
    a_bit = x & 1
    return (a_bit, b_bit, c_bit)

def set_row(row):
    a_bit, b_bit, c_bit = bits_from_int(row)
    GPIO.output(a_pin, a_bit)
    GPIO.output(b_pin, b_bit)
    GPIO.output(c_pin, c_bit)

def set_color_top(red_on, green_on, blue_on):
    GPIO.output(red1_pin, red_on)
    GPIO.output(green1_pin, green_on)
    GPIO.output(blue1_pin, blue_on)

def set_color_bottom(red_on, green_on, blue_on):
    GPIO.output(red2_pin, red_on)
    GPIO.output(green2_pin, green_on)
    GPIO.output(blue2_pin, blue_on)

def refresh():
    # NOTE: should only be called by the daemon thread
    # NOTE: OE is crucial here, it is low-active, so when it is
    # set to 0, the row on the pins shows
    refresh_start = time.time()
    for i in range(1,8):
    # to stick to convention we'll communicate in 8-bit color, but since
    # the hardware is slow, we'll really output in 3-bit color
    # by running a duty-cycle with 7 phases, so an LED can be on for 0-7 phases
        cycle_start = time.time()
        for row in range(8):
            # experimental
            # GPIO.output(oe_pin, 1)
            set_row(row)
            for col in range(32):
                top = screen[row][col]
                bottom = screen[row+8][col]
                # convert 8-bit to 3-bit color with a right shift
                set_color_top(top.red>>5 >= i, top.green>>5 >= i, top.blue>>5 >= i)
                set_color_bottom(bottom.red>>5 >= i, bottom.green>>5 >= i, bottom.blue>>5 >= i)
                clock()
            latch()
            GPIO.output(oe_pin, 0)
            time.sleep(delay)
            GPIO.output(oe_pin, 1)
        cycle_elapsed = time.time() - cycle_start
        #print('cycle ' + str(i) + ' in ' + str(cycle_elapsed) + 's')
    refresh_elapsed = time.time() -refresh_start
    #print('refreshed in ' + str(refresh_elapsed) + 's')

# NOTE: all ranges should be inclusive, so 
# fill_rectangle(0,0,1,1, Color(255,0,0)) should
# draw a 2x2 rectangle in the top left

def fill_rectangle(x1, y1, x2, y2, color):
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            screen[y][x] = color

def draw_line(x1, y1, x2, y2, color):
    slope = (y2-y1) / (x2-x1)
    for x in range(x1, x2+1):
        y = int(y1 + slope * (x-x1))
        screen[y][x] = color

def draw_rectangle(x1, y1, x2, y2, color):
    for x in range(x1, x2+1):
        screen[y1][x] = color
        screen[y2][x] = color
    for y in range(y1, y2+1):
        screen[y][x1] = color
        screen[y][x2] = color

def draw_circle(x_center, y_center, radius, color):
    for degree in range(360):
        x = radius*math.cos(math.radians(degree))
        y = radius*math.sin(math.radians(degree))
        screen[y][x] = color

def fill_circle(x_center, y_center, radius, color):
    for degree in range(360):
        x = radius*math.cos(math.radians(degree))
        y = radius*math.sin(math.radians(degree))

def write_char(x, y, c, color):
    bitmap = font.to_bitmap(c)
    for r in range(7):
        print(bitmap[r])
        for c in range(5):
            if bitmap[r][c] == 1:
                s = 'row=' + str(x+c) + '; col=' + str(y+r) + '; color=' + str(color)
                print(s)
                set_pixel(x+c, y+r, color)

def write_word(x, y, s, color):
   bitmap = font.to_bitmap(s)
   for row in range(len(bitmap)):
         for col in range(len(bitmap[row])):
            if 0 <= x+col and x+col < 32 and 0 <= y+row and y+row < 16 and bitmap[row][col]:
               set_pixel(x+col, y+row, color)

def scroll_text(x, y, s, color):
   for i in range(5*len(s)):
      fill_rectangle(x, y, 31, y+7, black)
      write_word(x-i, y, s, color)
      start = time.time()
      while(time.time() - start < 0.025):
          refresh()
      fill_rectangle(x, y, 31, y+7, black)

def set_pixel(x, y, color):
    screen[y][x] = color

def daemon_function():
    while True:
        refresh()


# fill_rectangle(0,0,31,15,purple)
# daemon_function()
# start a seperate thread of execution
# the daemon flag means it will stop when normal execution stops
# refresher = threading.Thread(target=daemon_function, daemon=True)
# refresher.start()
