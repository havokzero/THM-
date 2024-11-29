# TryHackMe Room Lookup Script

This Python script is designed for enumerating usernames on a login form for TryHackMe's "Room Lookup" challenge. It uses multithreading to efficiently send POST requests with usernames from a provided wordlist, checking for valid usernames.

## Features

- **Multithreading**: Utilizes up to 10 concurrent threads for faster enumeration.
- **Dynamic Console Output**: Displays progress in real-time, including the total usernames tried, the last username attempted, and elapsed time.
- **Custom Wordlist Support**: Reads usernames from a user-specified file path.
- **Error Handling**: Handles exceptions like missing files and HTTP request failures gracefully.

---

## How It Works

The script sends HTTP POST requests to the target URL with usernames from a wordlist. It checks the response for specific text ("Wrong password") to identify valid usernames.

---


## Script Parameters

- **`url`**: The target login URL. Set to `http://lookup.thm` in the script.
- **`file_path`**: Path to the wordlist file containing usernames.
- **`sem`**: Semaphore to limit concurrent threads (default is 10).

---

## Usage

1. Ensure the `requests` library is installed:
   ```bash
   pip install requests
   ```

2. Update the `url` and `file_path` variables in the script as needed.

3. Run the script:
   ```bash
   python3 script_name.py
   ```

4. Monitor the output to see the progress and found usernames.

---

## Output

The script dynamically updates the console with the following:
- Total usernames tried.
- Last username attempted.
- Elapsed time.

If valid usernames are found, they are displayed at the end of the script execution.

---

## Example

```plaintext
[*] Reading usernames from /usr/share/seclists/Usernames/Names/names.txt...
[*] Loaded 10000 usernames. Starting enumeration...

[*] Tried: 5000 / 10000, Last username: username         , Elapsed time: 12.34s

[*] Finished processing 10000 usernames in 25.67s.
[+] Found valid usernames:
    - username1
    - uisername2
```

---

## Customization

To use a different wordlist, update the `file_path` variable:
```python
file_path = "/path/to/your/wordlist.txt"
```

To change the number of concurrent threads, modify the semaphore:
```python
sem = threading.Semaphore(20)  # For 20 concurrent threads
```

---

## Notes

- This script is for **educational purposes only**. Ensure you have proper authorization before running it against any target.
- For larger wordlists, consider increasing the number of threads or using a more optimized tool.

---

## License

This project is open source and available under the [MIT License](LICENSE).
