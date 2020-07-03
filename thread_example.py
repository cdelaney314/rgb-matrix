import threading
import time

def daemon_function():
    while(True):
        print("daemon running...")
        time.sleep(0.25)

x = threading.Thread(target=daemon_function, daemon=True)
x.start()

print('running normal execution')
time.sleep(2)
print('normal execution complete')