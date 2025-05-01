from cryptography.fernet import Fernet

# Generate a new encryption key (store this securely)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Replace these with your actual bot token and chat ID
bot_token = "your telegram bot token"
chat_id = "your telegram chat id"

# Encrypt the bot token and chat ID
encrypted_bot_token = cipher_suite.encrypt(bot_token.encode())
encrypted_chat_id = cipher_suite.encrypt(chat_id.encode())

print(f"Encryption Key (store securely): {encryption_key.decode()}")
print(f"Encrypted Bot Token: {encrypted_bot_token.decode()}")
print(f"Encrypted Chat ID: {encrypted_chat_id.decode()}")
