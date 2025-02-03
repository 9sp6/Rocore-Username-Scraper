import requests
import os
import time
import random
import json
from colorama import Fore, Style, init

# Initialize Colorama for colored output
init(autoreset=True)

# =============================================================================
#                           Rocore Scraper
# =============================================================================
#
#              ██████╗░░█████╗░░█████╗░░█████╗░██████╗░███████╗
#              ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝
#              ██████╔╝██║░░██║██║░░╚═╝██║░░██║██████╔╝█████╗░░
#              ██╔══██╗██║░░██║██║░░██╗██║░░██║██╔══██╗██╔══╝░░
#              ██║░░██║╚█████╔╝╚█████╔╝╚█████╔╝██║░░██║███████╗
#              ╚═╝░░╚═╝░╚════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝
#
#                by Rocore Hub | Enjoy the Scrape!
# =============================================================================

# Display a fancy banner
def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}

██████╗░░█████╗░░█████╗░░█████╗░██████╗░███████╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝
██████╔╝██║░░██║██║░░╚═╝██║░░██║██████╔╝█████╗░░
██╔══██╗██║░░██║██║░░██╗██║░░██║██╔══██╗██╔══╝░░
██║░░██║╚█████╔╝╚█████╔╝╚█████╔╝██║░░██║███████╗
╚═╝░░╚═╝░╚════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝          
{Style.RESET_ALL}
"""
    print(banner)

# Load configuration from Configuration.json
def load_config():
    try:
        with open("Configuration.json", "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"{Fore.RED}{Style.BRIGHT}ERROR: Configuration.json file not found!{Style.RESET_ALL}")
        exit()
    except json.JSONDecodeError:
        print(f"{Fore.RED}{Style.BRIGHT}ERROR: Configuration.json file is not properly formatted!{Style.RESET_ALL}")
        exit()

# Constants from the config
config = load_config()
START_ID = config["start_id"]
END_ID = config["end_id"]
OUTPUT_FOLDER = config["output_folder"]

# Hacker-themed green text printing with borders
def print_hacker(text):
    border = f"{Fore.GREEN}{'-' * 60}{Style.RESET_ALL}"
    print(f"\n{border}")
    print(f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    print(border)

# Save valid usernames into year-specific files
def save_username(username, year, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, f"{year}.txt")
    with open(file_path, "a") as file:
        file.write(f"{username}\n")

# Fetch user data and filter banned accounts
def fetch_user_by_id(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("name", "Unknown")
            created_at = user_data.get("created", None)
            is_banned = user_data.get("isBanned", False)
            if not is_banned and created_at:
                year = created_at[:4]  # Extract year from creation date
                return username, year
        return None, None  # Skip banned or invalid users
    except requests.RequestException:
        pass  # Ignore failed requests
    return None, None

# Generate a random list of User IDs
def generate_random_ids(start, end, count=50000):
    return random.sample(range(start, end), min(count, end - start))

# Check if every year has at least one user
def ensure_year_coverage(years_collected):
    missing_years = [str(year) for year in range(2006, 2024) if str(year) not in years_collected]
    return missing_years

# Main scraper loop (original sequential mode)
def scrape_usernames(output_folder):
    print_hacker("Starting Roblox User ID Scraper...\n")
    years_collected = set()
    user_ids = generate_random_ids(START_ID, END_ID)
    total_ids = len(user_ids)
    
    try:
        for current_id in user_ids:
            print(f"{Fore.YELLOW}{Style.BRIGHT}Checking User ID: {current_id}{Style.RESET_ALL}")
            username, year = fetch_user_by_id(current_id)
            if username and year:
                save_username(username, year, output_folder)
                years_collected.add(year)
                print(f"{Fore.GREEN}  > Found: {username} (Created: {year}){Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  > User ID {current_id} is invalid, banned, or does not exist.{Style.RESET_ALL}")
            
            # Check for missing years periodically
            if len(years_collected) >= 15:  # Check coverage after 15 unique years
                missing_years = ensure_year_coverage(years_collected)
                if not missing_years:
                    print_hacker("\nAll years have at least one user! Ending scraper.")
                    break

            time.sleep(0.1)  # Prevent rate-limiting
    except KeyboardInterrupt:
        print_hacker("\nScraper stopped by user. Saving progress...\n")
    print_hacker("Scraping complete! Check the ScrapedFolder for results.\n")

# --- Additional Enhanced Features ---

import argparse
import logging

# Set up logging to file "scraper.log"
logging.basicConfig(filename="scraper.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# --- NEW FEATURE: PROXY SUPPORT ---
def load_proxies():
    """Load proxies from proxies.txt (one proxy per line)"""
    proxies = []
    if os.path.exists("proxies.txt"):
        with open("proxies.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    proxies.append(line)
    return proxies

def fetch_user_by_id_with_proxy(user_id, proxy):
    """Fetch user data using a given proxy"""
    url = f"https://users.roblox.com/v1/users/{user_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5, 
                                proxies={"http": proxy, "https": proxy})
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("name", "Unknown")
            created_at = user_data.get("created", None)
            is_banned = user_data.get("isBanned", False)
            if not is_banned and created_at:
                year = created_at[:4]
                return username, year
        return None, None
    except requests.RequestException:
        return None, None

# --- NEW FEATURE: CONCURRENT SCRAPING ---
def scrape_usernames_concurrent(output_folder, count=50000, threads=10, delay=0.1):
    """Scrape using multiple threads concurrently"""
    print_hacker("Starting Concurrent Roblox User ID Scraper...\n")
    years_collected = set()
    user_ids = generate_random_ids(START_ID, END_ID, count)
    total_ids = len(user_ids)
    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=total_ids, desc="Scraping", ncols=100)
    except ImportError:
        progress_bar = None
    
    import concurrent.futures
    def process_id(user_id):
        username, year = fetch_user_by_id(user_id)
        if username and year:
            save_username(username, year, output_folder)
            logging.info(f"Found {username} (Created: {year}) for ID {user_id}")
            return (user_id, username, year)
        else:
            logging.info(f"User ID {user_id} invalid or banned.")
            return None
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(process_id, uid): uid for uid in user_ids}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                _, _, year = result
                years_collected.add(year)
                print(f"{Fore.GREEN}Found user from year {year}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid or banned user{Style.RESET_ALL}")
            if progress_bar:
                progress_bar.update(1)
            time.sleep(delay)
            if len(years_collected) >= 15:
                missing_years = ensure_year_coverage(years_collected)
                if not missing_years:
                    print_hacker("\nAll years have at least one user! Ending concurrent scraper.")
                    break
    if progress_bar:
        progress_bar.close()
    print_hacker("Concurrent scraping complete! Check the ScrapedFolder for results.\n")

# --- NEW FEATURE: PROXY MODE SCRAPING ---
def scrape_usernames_with_proxies(output_folder, count=50000, delay=0.1):
    """Scrape using proxies from proxies.txt"""
    print_hacker("Starting Proxy-enabled Roblox User ID Scraper...\n")
    proxies = load_proxies()
    if not proxies:
        print(f"{Fore.RED}No proxies found in proxies.txt. Exiting proxy mode.{Style.RESET_ALL}")
        return
    years_collected = set()
    user_ids = generate_random_ids(START_ID, END_ID, count)
    total_ids = len(user_ids)
    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=total_ids, desc="Scraping with proxies", ncols=100)
    except ImportError:
        progress_bar = None
    
    for current_id in user_ids:
        proxy = random.choice(proxies)
        username, year = fetch_user_by_id_with_proxy(current_id, proxy)
        if username and year:
            save_username(username, year, output_folder)
            years_collected.add(year)
            print(f"{Fore.GREEN}Found: {username} (Created: {year}) using proxy {proxy}{Style.RESET_ALL}")
            logging.info(f"Found {username} (Created: {year}) for ID {current_id} using proxy {proxy}")
        else:
            print(f"{Fore.RED}User ID {current_id} invalid, banned, or does not exist. Proxy used: {proxy}{Style.RESET_ALL}")
            logging.info(f"Failed for user ID {current_id} using proxy {proxy}")
        if progress_bar:
            progress_bar.update(1)
        time.sleep(delay)
        if len(years_collected) >= 15:
            missing_years = ensure_year_coverage(years_collected)
            if not missing_years:
                print_hacker("\nAll years have at least one user! Ending proxy scraper.")
                break
    if progress_bar:
        progress_bar.close()
    print_hacker("Proxy scraping complete! Check the ScrapedFolder for results.\n")

# --- NEW MAIN WITH COMMAND-LINE ARGUMENTS ---
# Preserve the original main as "original_main" so it remains unchanged.
original_main = lambda: (
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'='*40}"),
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'      Welcome to Rocore Scraper!'}"),
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'='*40}{Style.RESET_ALL}\n"),
    print(f"{Fore.CYAN}{Style.BRIGHT}Tip:{Style.RESET_ALL} Press CTRL + C at any time to stop scraping.\n"),
    time.sleep(1),
    scrape_usernames(OUTPUT_FOLDER)
)

def main():
    global generate_random_ids  # Declare as global at the beginning of the function
    parser = argparse.ArgumentParser(description="Rocore Scraper Enhanced")
    parser.add_argument('--mode', choices=['normal', 'concurrent', 'proxy'], default='normal',
                        help="Scraping mode to use (default: normal)")
    parser.add_argument('--threads', type=int, default=10,
                        help="Number of threads for concurrent mode (default: 10)")
    parser.add_argument('--delay', type=float, default=0.1,
                        help="Delay between requests in seconds (default: 0.1)")
    parser.add_argument('--count', type=int, default=50000,
                        help="Number of random user IDs to check (default: 50000)")
    args = parser.parse_args()
    
    logging.info(f"Started scraper in mode {args.mode} with count {args.count} and delay {args.delay}")
    
    os.system("cls" if os.name=="nt" else "clear")
    print_banner()
    
    # Override generate_random_ids to use the provided count
    def generate_random_ids_override(start, end, count=args.count):
        return random.sample(range(start, end), min(count, end - start))
    
    generate_random_ids = generate_random_ids_override  # Reassign the global function
    
    if args.mode == 'normal':
        print(f"{Fore.CYAN}{Style.BRIGHT}Running in normal mode...{Style.RESET_ALL}\n")
        original_main()
    elif args.mode == 'concurrent':
        print(f"{Fore.CYAN}{Style.BRIGHT}Running in concurrent mode with {args.threads} threads...{Style.RESET_ALL}\n")
        scrape_usernames_concurrent(OUTPUT_FOLDER, count=args.count, threads=args.threads, delay=args.delay)
    elif args.mode == 'proxy':
        print(f"{Fore.CYAN}{Style.BRIGHT}Running in proxy mode...{Style.RESET_ALL}\n")
        scrape_usernames_with_proxies(OUTPUT_FOLDER, count=args.count, delay=args.delay)

if __name__ == "__main__":
    main()
