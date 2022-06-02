# Awning Safety Monitor
This is a script made to be run every X minutes (using cron-jobs) to check if an awning connected to a Somfy Tahoma Switch should be closed due to strong winds.

### API's used:
- Interaction with the awning is done using the [python-overkiz-api](https://github.com/iMicknl/python-overkiz-api).
- Weather data is fetched from the [SMHI Open Data API](https://opendata.smhi.se/apidocs/metfcst/index.html).
- Push-notifications are sent using [Pushover](https://pushover.net/).

## TODO:
- Create webserver to view logs and temporarily disable the safety script