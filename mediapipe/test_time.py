import time

start_time = time.time()  # get the current time

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time >= 10:
        print("This message is printed after a 10-second delay.")
        break