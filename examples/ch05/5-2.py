import time
import asyncio

async def task():
    print("Start of async task")
    await asyncio.sleep(5)
    print("Task resumde after 5 seconds")

async def spawn_tasks():
    await asyncio.gather(task(), task(), task())

start = time.time()
asyncio.run(spawn_tasks())
duration = time.time() - start

print(f"\nProcess completed in: {duration} seconds")