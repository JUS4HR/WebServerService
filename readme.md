Web server for running as systemd service
===
Usage
---
```
pip install -r requirements.txt
pyinstaller app.spec
./Scripts/install-service.sh
systemctl start webServer
```