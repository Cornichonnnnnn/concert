import threading
from concert.events import type as eventtype
from concert.base import ConcertObject


class UnknownStateError(Exception):
    """Any limit (hard or soft) exception."""
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message)


class State(object):
    """Status of a device.

    This is NOT a connection status, but a reflection of a physical device
    status. The implementation should follow this guideline.

    """
    ERROR = eventtype.make_event_id()
    
class Message(object):
    OUT_OF_RANGE = eventtype.make_event_id()
    INCOMPATIBLE_UNIT = eventtype.make_event_id()


class Device(ConcertObject):
    """Base class for controllable devices for which a set of parameters can be
    set.

    A :class:`Device` consists of optional getters, setters, limiters and units
    for named parameters. Implementations first call :meth:`__init__` and then
    :meth:`_register` to add or supplement a parameter.
    """

    def __init__(self):
        super(Device, self).__init__()
        self._setters = {}
        self._getters = {}
        self._limiters = {}
        self._units = {}

    def get(self, param):
        """Return the value of *param*."""
        if param not in self._getters:
            raise NotImplementedError

        return self._getters[param]()

    def set(self, param, value, blocking=False):
        """Set *param* to *value*.

        When *blocking* is true, execution stops until the hardware parameter
        is set to *value*.
        """
        if param not in self._setters:
            raise NotImplementedError

        if not self._unit_is_compatible(param, value):
            s = "`{0}' can only receive values of unit {1}"
            self.send(Message.INCOMPATIBLE_UNIT)
            if blocking:
                raise ValueError(s.format(param, self._units[param]))

        if not self._value_is_in_range(param, value):
            s = "Value {0} for `{1}` is out of range"
            self.send(Message.OUT_OF_RANGE)
            if blocking:
                raise ValueError(s.format(value, param))

        setter = self._setters[param]

        if blocking:
            setter(value)
        else:
            t = threading.Thread(target=setter, args=(value,))
            t.daemon = True
            t.start()

    def _unit_is_compatible(self, param, value):
        if not param in self._units:
            return True

        try:
            self._units[param] + value
            return True
        except:
            return False

    def _value_is_in_range(self, param, value):
        if param in self._limiters:
            return self._limiters[param](value)

        return True

    def _register_getter(self, param, getter):
        if param in self._getters:
            transform = self._getters[param]
            self._getters[param] = lambda: transform(getter())
        else:
            self._getters[param] = getter

    def _register_setter(self, param, setter):
        if param in self._setters:
            transform = self._setters[param]
            self._setters[param] = lambda arg: setter(transform(arg))
        else:
            self._setters[param] = setter

    def _register(self, param, getter, setter, unit, limiter=None):
        if getter:
            self._register_getter(param, getter)

        if setter:
            self._register_setter(param, setter)

        if unit:
            self._units[param] = unit

        if limiter:
            self._limiters[param] = limiter
