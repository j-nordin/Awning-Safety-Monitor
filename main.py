import asyncio
import os
from dotenv import load_dotenv
from pyoverkiz.const import SUPPORTED_SERVERS
from pyoverkiz.models import Command
import WindFetcher
from OverkizExtensions import OverkizClientExtension


def load_env_variables():
    dotenv_file = os.path.join(os.path.dirname(__file__), 'env_variables.env')
    load_dotenv(dotenv_file)


async def close_spa_awning(username,
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

        devices = await client.get_devices()

        for device in devices:
            print(f"{device.label} - {device.controllable_name}")
            print(device.device_url)
            for c in device.definition.commands:
                print(c)
            print(device.type)
            print("----")

        current_wind = WindFetcher.fetch_current_wind()

        if current_wind['wind_speed'] > unsafe_wind_speed or current_wind['wind_gust_speed'] > unsafe_wind_gust_speed:
            try:
                res = await client.execute_raw_commands(device_url=spa_awning_url,
                                                        commands=[Command("close")],
                                                        notification_type_mask=1,
                                                        notification_condition='ALWAYS',
                                                        notification_text='Closing the spa awning due to strong wind',
                                                        notification_title='Closing spa awning',
                                                        execution_mode='highPriority')
                print(res)
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

    await close_spa_awning(username,
                           password,
                           spa_awning_url,
                           unsafe_wind_speed=6,
                           unsafe_wind_gust_speed=9)


asyncio.run(main())
