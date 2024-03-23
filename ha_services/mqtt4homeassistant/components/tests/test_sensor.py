from unittest import TestCase

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from ha_services.mqtt4homeassistant.data_classes import ComponentConfig, ComponentState
from ha_services.mqtt4homeassistant.device import MqttDevice


class SensorTestCase(TestCase):
    def test_mimimal_sensor(self):
        sensor = Sensor(
            device=MqttDevice(name='My device', uid='device_id'),
            name='My component',
            uid='component_id',
        )
        self.assertEqual(
            sensor.get_config(),
            ComponentConfig(
                topic='homeassistant/sensor/device_id/device_id-component_id/config',
                payload={
                    'component': 'sensor',
                    'device': {'identifiers': 'device_id', 'name': 'My device'},
                    'device_class': None,
                    'json_attributes_topic': 'homeassistant/sensor/device_id/device_id-component_id/attributes',
                    'name': 'My component',
                    'state_class': None,
                    'state_topic': 'homeassistant/sensor/device_id/device_id-component_id/state',
                    'unique_id': 'device_id-component_id',
                    'unit_of_measurement': None,
                },
            ),
        )
        self.assertEqual(
            sensor.get_state(),
            ComponentState(topic='homeassistant/sensor/device_id/device_id-component_id/state', payload=None),
        )
        sensor.set_state(123)
        self.assertEqual(
            sensor.get_state(),
            ComponentState(topic='homeassistant/sensor/device_id/device_id-component_id/state', payload=123),
        )

    def test_full_sensor(self):
        sensor = Sensor(
            device=MqttDevice(name='My device', uid='device_id'),
            name='My component',
            uid='component_id',
            component='sensor',
            device_class='temperature',
            state_class='measurement',
            unit_of_measurement='°C',
            suggested_display_precision=2,
        )
        self.assertEqual(
            sensor.get_config(),
            ComponentConfig(
                topic='homeassistant/sensor/device_id/device_id-component_id/config',
                payload={
                    'component': 'sensor',
                    'device': {'identifiers': 'device_id', 'name': 'My device'},
                    'device_class': 'temperature',
                    'json_attributes_topic': 'homeassistant/sensor/device_id/device_id-component_id/attributes',
                    'name': 'My component',
                    'state_class': 'measurement',
                    'state_topic': 'homeassistant/sensor/device_id/device_id-component_id/state',
                    'suggested_display_precision': 2,
                    'unique_id': 'device_id-component_id',
                    'unit_of_measurement': '°C',
                },
            ),
        )
        self.assertEqual(
            sensor.get_state(),
            ComponentState(topic='homeassistant/sensor/device_id/device_id-component_id/state', payload=None),
        )
        sensor.set_state(456)
        self.assertEqual(
            sensor.get_state(),
            ComponentState(topic='homeassistant/sensor/device_id/device_id-component_id/state', payload=456),
        )
