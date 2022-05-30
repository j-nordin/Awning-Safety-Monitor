# Awning Safety Monitor
This is a script made to be run every X minutes (using for example cron-jobs) to check if the awning should be closed due to strong winds.

### Libraries used:
- Interaction with the awning is done using the [python-overkiz-api](https://github.com/iMicknl/python-overkiz-api).

- Weather data is fetched from the [SMHI Open Data API](https://opendata.smhi.se/apidocs/metfcst/index.html).

- Push-notifications are managed by [Pushover](https://pushover.net/).