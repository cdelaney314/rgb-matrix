import time
import matrixlib
import random

matrixlib.fill_rectangle(0,0,31,15, matrixlib.cyan)
time.sleep(2)
print('done rectange')
matrixlib.fill_rectangle(0,0,31,15, matrixlib.black)
for i in range(10):
    matrixlib.fill_rectangle(0,0,31,15, matrixlib.Color(random.randrange(255), random.randrange(255), random.randrange(255)))
    time.sleep(2)
    print(f'done rectange {i}')
matrixlib.fill_rectangle(0,0,31,15, matrixlib.black)
matrixlib.fill_circle(8,8,6, matrixlib.pink)
time.sleep(2)
print('done circle')
