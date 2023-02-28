import time
import threading
import SharedData

def read_thread(shared):
    while not exit.is_set():
        print(f"Read thread event loop: {shared.data}")
        time.sleep(0.5)

def update_thread(shared):
    while not exit.is_set():
        print(f"Update thread event loop: {shared.data}, adding 5")
        shared.update_value(shared.data + 5)
        time.sleep(0.33)

def start_threads():
    shared = SharedData()

    thread1 = threading.Thread(target = read_thread, args = (shared, ))
    thread1.start()

    thread2 = threading.Thread(target = update_thread, args = (shared, ))
    thread2.start()

    key = input("Enter any key to exit\n")
    print(f"You entered: {key}. Exiting")

    exit.set()
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    start_threads()