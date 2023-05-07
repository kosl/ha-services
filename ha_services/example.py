import dataclasses

from ha_services.mqtt4homeassistant.data_classes import MqttSettings


@dataclasses.dataclass
class MqttExampleValues:
    """
    Some values used to create DEMO MQTT messages.
    """

    mqtt_payload_prefix: str = 'example'
    device_name: str = 'ha-services-demo'


@dataclasses.dataclass
class DemoSettings:
    """
    This are just settings for the "ha-services" DEMO.
    Will be used in ha_services example commands.
    See "./cli.py --help" for more information.
    """

    mqtt: dataclasses = dataclasses.field(default_factory=MqttSettings)
    app: dataclasses = dataclasses.field(default_factory=MqttExampleValues)
