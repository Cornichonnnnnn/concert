"""
A device is an abstraction for a piece of hardware that can be controlled.

The main interface to all devices is a generic setter and getter mechanism.
:meth:`Device.set` sets a parameter to value. Additionally, you can specify a
*blocking* parameter to halt execution until the value is actually set on the
device::

    axis.set('position', 5.5 * q.mm, blocking=True)

    # This will be set once axis.set() has finished
    camera.set('exposure-time', 12.2 * q.s)

Some devices will provide convenience accessor methods. For example, to set the
position on an axis, you can also use :meth:`.Axis.set_position`.

:meth:`Device.get` simply returns the current value.
"""
import threading
import logging
from concert.base import Parameterizable
from concert.quantities import numerator_units, denominator_units


LOG = logging.getLogger(__name__)


class Device(Parameterizable):

    """
    A :class:`Device` provides locked access to a real-world device and
    provides a :attr:`state` :class:`.Parameter`.

    A implements the context protocol to provide locking and can be used like
    this ::

        with device:
            # device is locked
            device.parameter = 1 * q.m
            ...

        # device is unlocked again
    """

    def __init__(self):
        # We have to create the lock early on because it will be accessed in
        # any add_parameter calls, especially those in the Parameterizable base
        # class
        self._lock = threading.Lock()
        super(Device, self).__init__()

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._lock.release()


class Calibration(object):

    """Interface to convert between user and device units."""

    def __init__(self, user_unit, device_unit):
        self.user_unit = user_unit
        self.device_unit = device_unit

    def to_user(self, value):
        """Return *value* in user units."""
        raise NotImplementedError

    def to_device(self, value):
        """Return *value* in device units."""
        raise NotImplementedError


class LinearCalibration(Calibration):

    """A linear calibration maps a number of steps to a real-world unit.

    *steps_per_unit* tells how many steps correspond to some unit,
    *offset_in_steps* by how many steps the device is away from some zero
    point.
    """

    def __init__(self, device_units_per_user_units, offset_in_user_units):
        user_unit = denominator_units(device_units_per_user_units)
        device_unit = numerator_units(device_units_per_user_units)
        super(LinearCalibration, self).__init__(user_unit, device_unit)

        self.device_units_per_user_units = device_units_per_user_units
        self.offset = offset_in_user_units

    def to_user(self, value):
        return value / self.device_units_per_user_units - self.offset

    def to_device(self, value):
        result = (value + self.offset) * self.device_units_per_user_units

        # This can be done because to device go *always* counts
        return result.to_base_units()
