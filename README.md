![logo](assets/logo.png)

<a href="https://www.paypal.com/donate?hosted_button_id=VKCHVWUV48STE" target="_blank">
<img src="https://janbeta.net/wp-content/uploads/2020/06/Paypal-Donate.png" alt="Support me via PayPal" border="0" width="20%" height="20%"/>
</a>

# How to run
1. Install dependencies with `pip install -r requirements.txt`
2. Rename `config.example.json` to `config.json`, add your credentials to it
3. Run script with `python main.py`

# Notifications
Everything is handled through [Apprise](https://github.com/caronc/apprise).
Just add your `apprise.yaml`, basic `apprise.example.yaml` is available.

# ToDo:
- [ ] add project icon
- [ ] support other browsers (firefox for now)
- [ ] add optional arguments / options in configuration json
- [ ] rewrite `.bat` file, add bash script
