import requests
import os
import time
import random
import json
from colorama import Fore, Style, init

# Initialize Colorama for colored output
init(autoreset=True)

# Load configuration from Configuration.json
def load_config():
    try:
        with open("Configuration.json", "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"{Fore.RED}ERROR: Configuration.json file not found!{Style.RESET_ALL}")
        exit()
    except json.JSONDecodeError:
        print(f"{Fore.RED}ERROR: Configuration.json file is not properly formatted!{Style.RESET_ALL}")
        exit()

# Constants from the config
config = load_config()
START_ID = config["start_id"]
END_ID = config["end_id"]
OUTPUT_FOLDER = config["output_folder"]

# Hacker-themed green text
def print_hacker(text):
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

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

# Main scraper loop
def scrape_usernames(output_folder):
    print_hacker("Starting Roblox User ID Scraper...\n")
    years_collected = set()
    user_ids = generate_random_ids(START_ID, END_ID)
    total_ids = len(user_ids)
    
    try:
        for current_id in user_ids:
            print_hacker(f"Checking User ID: {current_id}")
            username, year = fetch_user_by_id(current_id)
            if username and year:
                save_username(username, year, output_folder)
                years_collected.add(year)
                print_hacker(f" > Found: {username} (Created: {year})")
            else:
                print(f"{Fore.RED} > User ID {current_id} is invalid, banned, or does not exist.{Style.RESET_ALL}")
            
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

# Options system
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print_hacker("========================================")
    print_hacker("             Rocore Scraper")
    print_hacker("========================================\n")
    
    print_hacker("Press CTRL + C at any time to stop scraping.\n")
    time.sleep(1)
    scrape_usernames(OUTPUT_FOLDER)

if __name__ == "__main__":
    main()
