![logo](logo.png)

# How to run
1. Download Chrome WebDriver from https://chromedriver.chromium.org and save it in script folder
2. Install dependencies with `pip install -r requirements.txt`
3. Run script with `python UTnotifier.py` (optional arguments available below)

# Arguments (use -h to see usage)
`--no_headless` - disables headless mode

`--disable_saving` - disables saving of login details (currently not implemented)

`--disable_mqtt` - disables publishing the test count to MQTT server

`--debug` - shows additional information like page refresh

# ToDo:
- [x] ~~write better README~~ done?
- [ ] check if one ***more*** or one ***less*** test is available
- [ ] make ***save credentials*** option (argument option?)
- [x] ~~make better logo (fix offset)~~
- [x] ~~make option for disabling headless mode (argument option?)~~
- [x] ~~add option to send notifications with MQTT (as sender.py ?)~~
