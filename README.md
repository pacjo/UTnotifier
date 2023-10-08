![logo](assets/logo.png)

<a href="https://www.paypal.com/donate?hosted_button_id=VKCHVWUV48STE" target="_blank">
<img src="https://janbeta.net/wp-content/uploads/2020/06/Paypal-Donate.png" alt="Support me via PayPal" border="0" width="20%" height="20%"/>
</a>

# How to run
1. Install dependencies with `pip install -r requirements.txt`
2. Run script with `python main.py`

# Arguments (use -h to see usage)
`--disable_headless` - disables headless mode

`--disable_saving` - disables saving of login details (currently not implemented)

`--disable_notifications` - disables showing notification when new test is available

`--debug` - shows additional information like page refresh

# Notifications
Everything is handled through [Apprise](https://github.com/caronc/apprise).
Just add your `apprise.yaml`, basic `apprise.example.yaml` is available.

# ToDo:
- [ ] add project icon
- [ ] support other browsers (firefox for now)
- [ ] add optional arguments / options in configuration json
- [ ] rewrite `.bat` file, add bash script
