import threading
import redis
from redis import ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0)
pool = ConnectionPool(host='localhost', port=6379, db=0)

def worker():
    r = redis.Redis(connection_pool=pool)
    r.set('key', 'value')
    print(f"Thread {threading.current_thread().name} completed")

threads = [threading.Thread(target=worker) for _ in range(5)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("All threads have finished.")
