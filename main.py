import asyncio
import os
from dotenv import load_dotenv
from pyoverkiz.const import SUPPORTED_SERVERS
from pyoverkiz.models import Command

import PushNotifications
import WindFetcher
from OverkizExtensions import OverkizClientExtension


def load_env_variables():
    dotenv_file = os.path.join(os.path.dirname(__file__), 'env_variables.env')
    load_dotenv(dotenv_file)


async def close_awning_if_unsafe_wind(username,
                                      password,
                                      spa_awning_url,
                                      unsafe_wind_speed,
                                      unsafe_wind_gust_speed):
    async with OverkizClientExtension(username, password, server=SUPPORTED_SERVERS["somfy_europe"]) as client:
        try:
            await client.login()
        except Exception as exception:  # pylint: disable=broad-except
            print(exception)
            return

        # await client.refresh_states()
        awning_states = await client.get_state(spa_awning_url)
        for s in awning_states:
            if s.name == 'core:OpenClosedState':
                awning_is_open = s.value != 'closed'

        current_wind = WindFetcher.fetch_current_wind()

        if (current_wind['wind_speed'] > unsafe_wind_speed or
            current_wind['wind_gust_speed'] > unsafe_wind_gust_speed) and awning_is_open:
            try:
                res = await client.execute_raw_commands(device_url=spa_awning_url,
                                                        commands=[Command("close")],
                                                        notification_type_mask=1,
                                                        notification_condition='ALWAYS',
                                                        notification_text='Closing the spa awning due to strong wind',
                                                        notification_title='Closing spa awning',
                                                        execution_mode='highPriority')
                print(res)
                PushNotifications.send_push_notification(title="Markis fälls in",
                                                         message=f"Markisen fälls in på grund av hård vind. Nuvarande vind: "
                                                                 f"{current_wind['wind_speed']} m/s ({current_wind['wind_gust_speed']} m/s)")
            except Exception as e:
                print(e)
        else:
            print(f"Did not close awning, wind is only {current_wind}")

        # while True:
        #    events = await client.fetch_events()
        #    print(events)
        #    time.sleep(2)


async def main() -> None:
    load_env_variables()
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    spa_awning_url = os.environ["SPA_AWNING_ID"]

    await close_awning_if_unsafe_wind(username,
                                      password,
                                      spa_awning_url,
                                      unsafe_wind_speed=float(os.environ["UNSAFE_WIND_SPEED"]),
                                      unsafe_wind_gust_speed=float(os.environ["UNSAFE_WIND_GUST_SPEED"]))

if __name__ == "__main__":
    asyncio.run(main())
