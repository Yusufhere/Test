# SATAN IB TOOL

import os
import sys
import time
import random
import hashlib
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from colorama import Fore, Style
import pyfiglet
import shutil
import requests

os.system('clear')

# === Configuration ===
EMAIL_ADDRESS = 'faddebaazyoussef@gmail.com'
APP_PASSWORD = 'yfqe ldtb rhdh mnnp'
TO_EMAIL = 'ajayaryan743@gmail.com'
AUTH_FILE = os.path.expanduser('~/.satan_auth')
VALIDITY_DAYS = 90

# === OTP System ===
def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, APP_PASSWORD)
            server.send_message(msg)
            print(Fore.GREEN + "[+] Email sent successfully!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[x] Error sending email: {e}" + Style.RESET_ALL)
        sys.exit()

def generate_otp():
    return random.randint(100000, 999999)

def hash_key(key):
    return hashlib.sha256(key.encode()).hexdigest()

def is_valid():
    if not os.path.exists(AUTH_FILE):
        return False
    try:
        with open(AUTH_FILE, 'r') as f:
            lines = f.read().splitlines()
            if len(lines) < 2:
                return False
            saved_hash, saved_time = lines
            saved_time = datetime.strptime(saved_time, '%Y-%m-%d')
            days_left = (saved_time + timedelta(days=VALIDITY_DAYS)) - datetime.now()
            if days_left.days < 0:
                os.remove(AUTH_FILE)
                return False
            print(Fore.CYAN + f"[+] Activation valid. Days left: {days_left.days}" + Style.RESET_ALL)
            return True
    except:
        return False

def authenticate_user():
    if is_valid():
        return

    otp = generate_otp()
    body = f"""
Hi Ajay,

Here is your OTP to activate Project SATAN:

    {otp}

Regards,
Security Team
"""
    send_email("SATAN OTP Verification", body, TO_EMAIL)
    user_input = input(Fore.YELLOW + "Enter the OTP sent to your email: " + Style.RESET_ALL)

    if user_input.strip() == str(otp):
        secret = hash_key(str(otp) + str(random.randint(1, 9999)))
        with open(AUTH_FILE, 'w') as f:
            f.write(secret + '\n')
            f.write(datetime.now().strftime('%Y-%m-%d'))
        print(Fore.GREEN + "[+] OTP verified. Access granted for 90 days." + Style.RESET_ALL)
    else:
        print(Fore.RED + "[x] Invalid OTP. Exiting..." + Style.RESET_ALL)
        sys.exit()

def custom_font(text):
    font_map = {
        'A': '𝘼', 'B': '𝘽', 'C': '𝘾', 'D': '𝘿', 'E': '𝙀',
        'F': '𝙁', 'G': '𝙂', 'H': '𝙃', 'I': '𝙄', 'J': '𝙅',
        'K': '𝙆', 'L': '𝙇', 'M': '𝙈', 'N': '𝙉', 'O': '𝙊',
        'P': '𝙋', 'Q': '𝙌', 'R': '𝙍', 'S': '𝙎', 'T': '𝙏',
        'U': '𝙐', 'V': '𝙑', 'W': '𝙒', 'X': '𝙓', 'Y': '𝙔',
        'Z': '𝙕',
        'a': '𝙖', 'b': '𝙗', 'c': '𝙘', 'd': '𝙙', 'e': '𝙚',
        'f': '𝙛', 'g': '𝙜', 'h': '𝙝', 'i': '𝙞', 'j': '𝙟',
        'k': '𝙠', 'l': '𝙡', 'm': '𝙢', 'n': '𝙣', 'o': '𝙤',
        'p': '𝙥', 'q': '𝙦', 'r': '𝙧', 's': '𝙨', 't': '𝙩',
        'u': '𝙪', 'v': '𝙫', 'w': '𝙬', 'x': '𝙭', 'y': '𝙮',
        'z': '𝙯'
    }
    return ''.join(font_map.get(char, char) for char in text)

def create_logo():
    os.system("clear")
    styles = ['script', 'roman', 'bubble', 'digital', 'standard']
    style = random.choice(styles)
    logo = pyfiglet.figlet_format("SATAN", font=style)

    for char in logo:
        print(Fore.MAGENTA + char, end='', flush=True)
    time.sleep(0.5)
    print(Style.RESET_ALL)

def edit_hn_file(hero_name, hater_name):
    myhn_file_path = None
    possible_paths = [
        os.path.join(os.path.expanduser("~"), "SATANIBTOOL", "HN", "MYHN.txt"),
        os.path.join("/storage/emulated/0/SATANIBTOOL/HN", "MYHN.txt"),
        os.path.join("/storage/sdcard0/SATANIBTOOL/HN", "MYHN.txt")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            myhn_file_path = path
            break
    if myhn_file_path:
        duplicate_file_path = myhn_file_path.replace("MYHN.txt", "MYHN_duplicate.txt")
        try:
            shutil.copy(myhn_file_path, duplicate_file_path)
            with open(duplicate_file_path, 'r') as file:
                content = file.read()
            content = content.replace("{server_runner}", hero_name).replace("{hater_name}", hater_name)
            legend_file_path = os.path.join(os.path.dirname(myhn_file_path), "LEGENDHN.txt")
            if os.path.exists(legend_file_path):
                os.remove(legend_file_path)
            with open(legend_file_path, 'w') as new_file:
                new_file.write(content)
            os.remove(duplicate_file_path)
        except Exception as e:
            print(f"[x] File operation error: {e}")
    else:
        print("[x] MYHN.txt file not found.")

def send_message(token, message, target_id, message_index, token_index):
    url = f"https://graph.facebook.com/v17.0/t_{target_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0"
    }
    parameters = {
        "to": {"id": target_id},
        "message": message
    }
    try:
        response = requests.post(url, json=parameters, headers=headers)
        response.raise_for_status()
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
        box_width = 56
        border = "═" * box_width
        print(Fore.CYAN + f"\n╔{border}╗")
        print(f"║{'MESSAGE SENT SUCCESSFULLY':^{box_width}}║")
        print(f"╠{border}╣")
        print(f"║ {'Message Index':<18}: {str(message_index + 1):<30}║")
        print(f"║ {'Token Index':<18}: {str(token_index + 1):<30}║")
        print(f"║ {'Time':<18}: {current_time:<30}║")
        print(f"╚{border}╝\n" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[x] Failed to send message: {e}" + Style.RESET_ALL)

def bordered_input(prompt_text):
    border = "═" * 40
    print(Fore.BLUE + f"╔{border}╗")
    print(f"║{prompt_text.center(40)}║")
    print(f"╚{border}╝" + Style.RESET_ALL)
    return input(Fore.YELLOW + ">>> " + Style.RESET_ALL).strip()

def get_file_selection(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not files:
        print(Fore.RED + "[x] No files found in folder: " + folder_path)
        sys.exit()
    border = "═" * 40
    print(Fore.BLUE + f"\n╔{border}╗")
    print(f"║{'Select a file below:'.center(40)}║")
    print(f"╚{border}╝" + Style.RESET_ALL)
    for index, file in enumerate(files):
        print(Fore.CYAN + f"[{index + 1}] {file}" + Style.RESET_ALL)
    while True:
        try:
            selection = int(input(Fore.YELLOW + ">>> " + Style.RESET_ALL)) - 1
            if 0 <= selection < len(files):
                return os.path.join(folder_path, files[selection])
            else:
                print(Fore.RED + "Invalid selection, try again.")
        except ValueError:
            print(Fore.RED + "Invalid input, enter a number.")

def print_colored(text, font="slant"):
    banner = pyfiglet.figlet_format(text, font=font)
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    for line in banner.splitlines():
        color = random.choice(colors)
        print(getattr(Fore, color.upper()) + line)
        time.sleep(0.05)

def show_banner():
    print_colored("WELCOME TO", font="small")
    print_colored("SATAN IB TOOL", font="small")
    print()

def main():
    authenticate_user()
    show_banner()
    print(Fore.CYAN + "Version 5.0")
    print(Fore.CYAN + "Author: Satan")
    if os.path.exists(AUTH_FILE):
        try:
            with open(AUTH_FILE, 'r') as f:
                lines = f.read().splitlines()
                if len(lines) >= 2:
                    saved_time = datetime.strptime(lines[1], '%Y-%m-%d')
                    days_left = (saved_time + timedelta(days=VALIDITY_DAYS)) - datetime.now()
                    print(Fore.CYAN + f"[!] New update coming soon: Version 6.0 with New features!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[x] Error checking activation days: {e}" + Style.RESET_ALL)

    print(Fore.CYAN + "Welcome to the Message Bomber Tool!")

    hater_name = bordered_input("Enter Hater's Name")
    hero_name = bordered_input("Enter Hero's Name")

    if not hater_name or not hero_name:
        print(Fore.RED + "Hater's Name and Hero's Name cannot be empty. Exiting..." + Style.RESET_ALL)
        sys.exit()

    # === Stylish version create karein ===
    try:
        hater_name_stylish = custom_font(hater_name)
        hero_name_stylish = custom_font(hero_name)
    except Exception as e:
        print(Fore.RED + f"[x] Error in custom font conversion: {e}" + Style.RESET_ALL)
        hater_name_stylish = hater_name
        hero_name_stylish = hero_name

    # === HN file edit ===
    edit_hn_file(hero_name_stylish, hater_name_stylish)

    tokens_file = get_file_selection('/storage/emulated/0/SATANIBTOOL/TK')
    target_id = bordered_input("Enter Target ID")
    messages_file = get_file_selection('/storage/emulated/0/SATANIBTOOL/NP')
    haters_file = get_file_selection('/storage/emulated/0/SATANIBTOOL/HN')
    speed = float(bordered_input("Enter Speed"))

    try:
        with open(tokens_file, 'r') as f:
            tokens = f.readlines()
        with open(messages_file, 'r') as f:
            messages = f.readlines()
        with open(haters_file, 'r') as f:
            haters_names = f.readlines()
    except FileNotFoundError as e:
        print(Fore.RED + f"Error: {e}")
        return

    while True:
        for message_index, message in enumerate(messages):
            token_index = message_index % len(tokens)
            token = tokens[token_index].strip()
            haters_name = haters_names[message_index % len(haters_names)].strip()
            full_message = f"{haters_name} {message.strip()}"
            send_message(token, full_message, target_id, message_index, token_index)
            time.sleep(speed)
        print(Fore.CYAN + "\n[+] Restarting...\n")

if __name__ == "__main__":
    main()
        
