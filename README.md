# Firewall_MITMProxy
Web application for blocking ads and web-sites that contain unwanted words using a MITM Proxy firewall.

## How to configure the project



1. Create these files in the project directory "banned_words.log", "blocked_ads.log" "blocked_websites.log" and "ad_rules.log"


2. Go to the Command Prompt, right-click it and press 'Run as Administrator', go to the project directory and type these commands:
    - python -m venv venv   (To create the venv if it is not created already in this folder)
    - cd venv/Scripts (Go in the venv/Scripts directory)
    - activate.bat  (activate the folder's venv)
    - cd ../..  (going back to the project directory)
    - pip install flask flask-cors mitmproxy requests adblockparser  (to download the 'flask-cors' library in the venv if it's not already installed)


3. Run in the cmd as an administrator this command if you want to run the project:
   - python run_script.py
     (or if you want to open the mitmproxy web interface too, where you can see the internet traffic and all the flows, you can run this command)
   - python run_script_web.py