from pprint import pprint
from typing import cast

from pyoverkiz.client import OverkizClient
from pyoverkiz.models import Command

# https://github.com/iMicknl/python-overkiz-api - API used for interacting with the tahoma box


class AdvancedCommand(Command):
    """ Class for extended commands """
    command_type: int
    delay: int

    def __init__(self,
                 name: str,
                 parameters: list[str | int | float],
                 command_type: int = 1,
                 delay: int = 0):
        super().__init__(name, parameters)
        self.command_type = command_type
        self.delay = delay
        dict.__init__(self, name=name, parameters=parameters, delay=delay, command_type=command_type)


class OverkizClientExtension(OverkizClient):
    """ Extension of the OverkizClient to enable sending extended commands to a device """

    async def execute_raw_commands(self,
                                   device_url: str,
                                   commands: list[Command | AdvancedCommand],
                                   notification_type_mask: int = 0,
                                   notification_text: str | None = None,
                                   notification_title: str | None = None,
                                   notification_condition: str | None = None,
                                   label: str = "python-overkiz-api-raw-command",
                                   execution_mode: str = None
                                   ) -> str:
        """ Method for sending commands to a device """
        should_notify = (notification_type_mask and
                         notification_condition and
                         notification_text and
                         notification_condition)

        payload = {
            'label': label,
            'actions': [{'deviceURL': device_url, 'commands': commands}]
        }

        if should_notify:
            payload['notificationTypeMask'] = notification_type_mask
            payload['notificationText'] = notification_text
            payload['notificationTitle'] = notification_title
            payload['notificationCondition'] = notification_condition

        # use parent post method
        response: dict = await self._OverkizClient__post(
            path=f"exec/apply/{execution_mode}" if execution_mode else "exec/apply",
            payload=payload)
        return cast(str, response["execId"])
