# Awning Safety Monitor
This is a script made to be run every X minutes (using for example cron-jobs) to check if the awning should be closed due to strong winds.

The interaction with the awning is done using the [python-overkiz-api](https://github.com/iMicknl/python-overkiz-api)

The weather data is fetched from the [SMHI Open Data API](https://opendata.smhi.se/apidocs/metfcst/index.html)