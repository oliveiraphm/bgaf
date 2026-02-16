import time

def task():
    print("Start of sync task")
    time.sleep(5)
    print("After 5 seconds of sleep")

start = time.time()
for _ in range(3):
    task()
duration = time.time() - start
print(f"Process completed in: {duration} seconds")