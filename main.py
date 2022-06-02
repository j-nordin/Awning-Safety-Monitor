import asyncio
import logging
import os
from dotenv import load_dotenv
from pyoverkiz.const import SUPPORTED_SERVERS
from pyoverkiz.models import Command

import LoggingConfigurator
import PushNotifications
import WindFetcher
from OverkizExtensions import OverkizClientExtension


def _load_env_variables():
    dotenv_file = os.path.join(os.path.dirname(__file__), 'env_variables.env')
    load_dotenv(dotenv_file)


async def close_awning_if_unsafe_wind(username,
                                      password,
                                      spa_awning_url,
                                      unsafe_wind_speed,
                                      unsafe_wind_gust_speed):
    logging.info("-------------------------- STARTING AWNING CHECK --------------------------")
    async with OverkizClientExtension(username, password, server=SUPPORTED_SERVERS["somfy_europe"]) as client:
        try:
            logging.info("Logging in to somfy...")
            await client.login()
            logging.info("Login successful")
        except Exception:  # pylint: disable=broad-except
            logging.exception("Client could not log in")

        try:
            logging.info("Checking awning current state...")
            # await client.refresh_states()
            awning_states = await client.get_state(spa_awning_url)
            for s in awning_states:
                if s.name == 'core:OpenClosedState':
                    awning_is_open = s.value != 'closed'
            logging.info(f"Awning is currently: {'open' if awning_is_open else 'closed'}")
        except Exception:
            logging.exception("Awning-state could not be checked")

        logging.info("Checking current weather conditions...")
        current_wind = WindFetcher.fetch_current_wind()
        logging.info(f"Current weather conditions: {current_wind}")

        if (current_wind['wind_speed'] > unsafe_wind_speed or
            current_wind['wind_gust_speed'] > unsafe_wind_gust_speed) and awning_is_open:
            try:
                logging.info("Awning is being closed due to hard wind...")
                await client.execute_raw_commands(device_url=spa_awning_url,
                                                  commands=[Command("close")],
                                                  execution_mode='highPriority')
                logging.info("Command to close awning successfully sent")
            except Exception:
                PushNotifications.send_push_notification(title="Markis kunde inte fällas in",
                                                         message="Kommando för att stänga markisen kunde inte skickas")
                logging.exception("Command to close awning could not be sent")

            try:
                logging.info("Send push notification about closing the awning")
                PushNotifications.send_push_notification(title="Markis fälls in",
                                                         message=f"Markisen fälls in på grund av hård vind. Nuvarande vind: "
                                                                 f"{current_wind['wind_speed']} m/s ({current_wind['wind_gust_speed']} m/s)")
            except Exception:
                logging.exception("Push notification about closing the awning could not be sent")
        else:
            logging.info(
                f"Did not close awning, wind is {current_wind} and state of the awning is: {'open' if awning_is_open else 'closed'}")


async def main() -> None:
    _load_env_variables()
    LoggingConfigurator.config_logging()
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    spa_awning_url = os.environ["SPA_AWNING_ID"]

    try:
        await close_awning_if_unsafe_wind(username,
                                          password,
                                          spa_awning_url,
                                          unsafe_wind_speed=float(os.environ["UNSAFE_WIND_SPEED"]),
                                          unsafe_wind_gust_speed=float(os.environ["UNSAFE_WIND_GUST_SPEED"]))
    except Exception:
        logging.exception("Something while checking the awning went wrong")


if __name__ == "__main__":
    asyncio.run(main())
