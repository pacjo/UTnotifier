import apprise

def apprise_notify(config_filepath, number_of_tests):
    # Create an Apprise instance
    ar = apprise.Apprise()

    # Create an Config instance
    arconfig = apprise.AppriseConfig()

    # Add a configuration source:
    arconfig.add(config_filepath)

    # Make sure to add our config into our apprise object
    ar.add(arconfig)

    # Notify
    ar.notify(
        title='UTnotifier',
        body=f'New test available, number of tests: {number_of_tests}',
    )
