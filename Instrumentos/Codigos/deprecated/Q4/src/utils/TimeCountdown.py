import time


def sleep(seconds: float):
    for i in range(seconds, 0, -1):
        print(f"{i}", end="\r", flush=True)
        time.sleep(1)
