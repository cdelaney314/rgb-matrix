import RPi.GPIO as GPIO
import time
import font

delay = 1 / (1*1000000)
#delay = 3

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

screen = [[0 for x in xrange(32)] for x in xrange(16)]

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

def set_color_top(color):
    blue, green, red = bits_from_int(color)
    GPIO.output(red1_pin, red)
    GPIO.output(green1_pin, green)
    GPIO.output(blue1_pin, blue)

def set_color_bottom(color):
    blue, green, red = bits_from_int(color)
    GPIO.output(red2_pin, red)
    GPIO.output(green2_pin, green)
    GPIO.output(blue2_pin, blue)

def refresh():
    # NOTE: OE is crucial here, it is low-active, so when it is
    # set to 0, the row on the pins shows
    for row in range(8):
        set_row(row)

        for col in range(32):
            set_color_top(screen[row][col])
            set_color_bottom(screen[row+8][col])
            clock()

        latch()
	GPIO.output(oe_pin, 0)
        time.sleep(delay)
        GPIO.output(oe_pin, 1)

def fill_rectangle(x1, y1, x2, y2, color):
    for x in range(x1, x2):
        for y in range(y1, y2):
            screen[y][x] = color

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

def scroll_word(x, y, s, color):
   for i in range(5*len(s)):
      fill_rectangle(x, y, 32, y+7, 0)
      write_word(x-i, y, s, color)
      start = time.time()
      while(time.time() - start < 0.025):
	refresh()
      fill_rectangle(x, y, 32, y+7, 0)

def set_pixel(x, y, color):
    screen[y][x] = color

#fill_rectangle(0,0,32,16,4)
scroll_word(0,0,'It works!', 7)
'''while True:
	refresh()'''
