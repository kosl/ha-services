from __future__ import annotations

import dataclasses
import logging
import socket
from typing import TypeAlias

from bx_py_utils.anonymize import anonymize

from ha_services.mqtt4homeassistant.utilities.string_utils import slugify


logger = logging.getLogger(__name__)


StatePayload: TypeAlias = str | bytes | bytearray | int | float | None


class NoState:
    """
    This is a special value that indicates that the state has not been set yet.
    It is used to avoid publishing an empty state to Home Assistant.
    """

    def __repr__(self):
        return '<NoState>'


NO_STATE = NoState()


@dataclasses.dataclass
class ComponentState:
    topic: str
    payload: StatePayload


@dataclasses.dataclass
class ComponentConfig:
    topic: str
    payload: dict


@dataclasses.dataclass
class MqttSettings:
    """
    Credentials to MQTT server that should be used.

    The `main_uid` is used as a second prefix for all MQTT messages, to avoid conflicts.

    With `publish_config_throttle_seconds` you can set the throttle interval
    for publishing config messages to Home Assistant.
    """

    host: str = 'mqtt.eclipseprojects.io'  # public test MQTT broker service
    port: int = 1883
    user_name: str = ''
    password: str = ''

    main_uid: str = dataclasses.field(default_factory=socket.gethostname)
    publish_config_throttle_seconds: int = 20

    def __post_init__(self):
        assert self.main_uid, 'main_uid must be provided'

        main_uid = slugify(self.main_uid, sep='_')
        if main_uid != self.main_uid:
            self.main_uid = main_uid
            logger.warning('main_uid has been slugified to: %r', self.main_uid)

    def anonymized(self):
        data = dataclasses.asdict(self)
        if self.password:
            data['password'] = anonymize(self.password)
        return data
