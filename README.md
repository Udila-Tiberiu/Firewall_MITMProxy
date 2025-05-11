# Firewall_MITMProxy
Web application for blocking ads and web-sites that contain unwanted words using a MITM Proxy firewall.

## How to configure the project

1. Go to the 'mitm_proxy' folder in terminal and type these commands:
   - python -m venv venv    (To create the venv if it is not created already)
   - venv/Scripts/activate  (activate the folder's venv)
   - pip install mitmproxy  (to download the 'mitmproxy' library in the venv if it's not already installed)

2. Go to the 'server' folder in terminal and type these commands:
    - python -m venv venv   (To create the venv if it is not created already in this folder)
    - venv/Scripts/activate  (activate the folder's venv)
    - pip install flask-cors (to download the 'flask-cors' library in the venv if it's not already installed)
