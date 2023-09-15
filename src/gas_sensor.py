import asyncio
from typing import Any, ClassVar, Dict, Mapping, Optional
from viam.components.sensor import Sensor
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from enviroplus import gas


class MySensor(Sensor):
    # Subclass the Viam Arm component and implement the required functions
    MODEL: ClassVar[Model] = Model(ModelFamily("tuneni", "gas_sensor"), "linux")

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        sensor = cls(config.name)
        return sensor

    async def get_readings(self, **kwargs):
        nh3_readings = []
        ox_readings = []
        red_readings = []

        nh3_readings.append(gas.read_nh3())
        ox_readings.append(gas.read_oxidising())
        red_readings.append(gas.read_reducing())

        data = {'nh3': nh3_readings, 'ox': ox_readings, 'red': red_readings}

        return data


async def main():
    gas = MySensor(name="gas")
    signal = await gas.get_readings()
    print(signal)


if __name__ == '__main__':
    asyncio.run(main())

