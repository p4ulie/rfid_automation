# Installation

**_NOTE: User running the installation script needs to be sudo-capable._** 

```shell
git clone https://github.com/p4ulie/rfid_automation.git
cd rfid_automation
sudo ./install.sh
```

[Installer script](install.sh):
* copies application files to the _/usr/bin/rfid_automation_ directory
* application desktop entry (icon, system menu item for application) _rfid_automation.desktop_ into _/usr/share/applications/_
* sets the permissions of files to enable execution

# Update

```shell
cd rfid_automation
git pull
sudo ./install.sh
```
