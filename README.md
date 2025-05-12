# Firewall_MITMProxy
Web application for blocking ads and web-sites that contain unwanted words using a MITM Proxy firewall.

## How to configure the project



1. Create these files in the project directory "banned_words.log", "blocked_ads.log" "blocked_websites.log"


2. Go to the terminal in the project directory and type these commands:
    - python -m venv venv   (To create the venv if it is not created already in this folder)
    - venv/Scripts/activate  (activate the folder's venv)
    - pip install flask flask-cors mitmproxy  (to download the 'flask-cors' library in the venv if it's not already installed)


3. Run in the cmd as an administrator this commands if you want to run the project:
   - python run_script.py