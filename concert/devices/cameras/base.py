"""
A :class:`Camera` can be set via the device-specific properties that can be set
and read with :meth:`.Device.set` and :meth:`.Device.get`. Moreover, a camera
provides means to

* :meth:`record` frames,
* :meth:`stop` the acquisition and
* :meth:`trigger` a frame capture.

To setup and use a camera in a typical environment, you would do::

    from concert.devices.cameras.uca import UcaCamera

    camera = UcaCamera('pco')
    camera.set('exposure-time', 0.2 * q.s)
    camera.record()
    camera.trigger(blocking=True)
    camera.stop()
"""

from concert.base import launch
from concert.devices.base import Device


class Camera(Device):
    """Base class for remotely controllable cameras."""

    def __init__(self):
        super(Camera, self).__init__()

    def record(self, blocking=False):
        """Start recording frames."""
        launch(self._record_real, blocking=blocking)

    def stop(self, blocking=False):
        """Stop recording frames."""
        launch(self._stop_real, blocking=blocking)

    def trigger(self, blocking=False):
        """Trigger a frame if possible."""
        launch(self._trigger_real, blocking=blocking)

    def _record_real(self):
        raise NotImplemented

    def _stop_real(self):
        raise NotImplemented

    def _trigger_real(self):
        raise NotImplemented
