import requests
import time
import multiprocessing
import logging
from tqdm import tqdm  
import os
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of test URLs
test_urls = [
    "https://ipinfo.io/json",
    "https://httpbin.org/get",
    "https://api.ipify.org?format=json",
    "https://www.google.com"
]

def load_proxies_from_file(filename):
    """Load proxies from a given file."""
    with open(filename, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def check_proxy(proxy):
    """Check the response time of a proxy for multiple URLs."""
    results = []
    for url in test_urls:
        start_time = time.time()
        try:
            logging.info(f"Testing proxy: {proxy} with URL: {url}")
            response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
            response_time = time.time() - start_time
            logging.info(f"Proxy {proxy} responded with status code {response.status_code} in {response_time:.2f} seconds.")
            results.append((proxy, url, response.status_code, response_time))
        except requests.RequestException:
            logging.warning(f"Proxy {proxy} failed to respond for URL: {url}.")
            results.append((proxy, url, None, None))
    return results

def clear_console():
    # Clear console based on the operating system
    if os.name == 'nt':
        os.system('cls')  # For Windows
    else:
        os.system('clear')

from tqdm import tqdm
import multiprocessing

def benchmark_proxies(proxies):
    results = []
    
    with tqdm(total=len(proxies), desc="Testing Proxies", position=0, dynamic_ncols=True) as pbar:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            for proxy, result in zip(proxies, pool.imap(check_proxy, proxies)):
                # Clear the console before updating the progress bar
                clear_console()  
                results.extend(result)  # Append multiple results for each proxy
                pbar.update(1)  

    return results

def save_results_to_file(results, filename):
    """Save benchmarking results to a file."""
    valid_results = [(proxy, url, status_code, response_time) for proxy, url, status_code, response_time in results if status_code is not None]
    sorted_results = sorted(valid_results, key=lambda x: x[3])  # Sort by response time

    with open(filename, 'a') as file:
        for proxy, url, status_code, response_time in sorted_results:
            file.write(f"{proxy}\n")

if __name__ == "__main__":
    proxies_file = r"Proxies/Free_Proxy_List.txt"
    proxies = load_proxies_from_file(proxies_file)
    
    logging.info("Starting proxy benchmarking...")
    benchmark_results = benchmark_proxies(proxies)

    # Save the results to a file
    output_file = "proxy_benchmark_results.txt"
    save_results_to_file(benchmark_results, output_file)

    logging.info(f"Results saved to {output_file}.")
