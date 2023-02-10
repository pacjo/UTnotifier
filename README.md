![logo](assets/logo.png)

<a href="https://www.paypal.com/donate?hosted_button_id=VKCHVWUV48STE" target="_blank">
<img src="https://janbeta.net/wp-content/uploads/2020/06/Paypal-Donate.png" alt="Support me via PayPal" border="0" width="20%" height="20%"/>
</a>

[![my-ha blueprint badge](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/pacjo/UTnotifier/main/addons/UTnotifier_HA_blueprint.yaml)

# How to run
1. Install dependencies with `pip install -r requirements.txt`
2. Run script with `python UTnotifier.py` (optional arguments available below)

# Arguments (use -h to see usage)
`--disable_headless` - disables headless mode

`--disable_saving` - disables saving of login details (currently not implemented)

`--disable_notifications` - disables showing notification when new test is available

`--debug` - shows additional information like page refresh

# Notifications
Everything is handled through [Apprise](https://github.com/caronc/apprise).
Just add Apprise URLs to `credentials.json` as shown is `STOCkcredentials.json`

# ToDo:
- [ ] make sure MQTT message are received
- [x] ~~add project icon~~
- [ ] properly kill webdriver
- [x] add MQTT TLS support
- [x] rewrite login to support multiple tries
- [x] add notification instructions