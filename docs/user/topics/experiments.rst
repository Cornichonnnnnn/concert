===========
Experiments
===========

Experiments connect data acquisition and processing. They can be run multiple times
by the :meth:`.base.Experiment.run`, they take care of proper file structure and
logging output.


Acquisition
-----------

Experiments consist of :class:`.Acquisition` objects which encapsulate data generator
and consumers for a particular experiment part (dark fields, radiographs, ...). This
way the experiments can be broken up into smaller logical pieces. A single acquisition
object needs to be reproducible in order to repeat an experiment more times, thus we
specify its generator and consumers as callables which return the actual generator or
consumer. We need to do this because generators cannot be "restarted".

It is very important that you enclose the executive part of the production and
consumption code in `try-finally` to ensure proper clean up. E.g. if a producer
starts rotating a motor, then in the `finally` clause there should be the call
`motor.stop().join()`.

An example of an acquisition could look like this::

    from concert.coroutines.base import coroutine
    from concert.experiments.base import Acquisition

    # This is a real generator, num_items is provided somewhere in our session
    def produce():
        try:
            for i in range(num_items):
                yield i
        finally:
            # Clean up here

    # A simple coroutine sink which prints items
    @coroutine
    def consumer():
        try:
            while True:
                item = yield
                print item
        finally:
            # Clean up here

    acquisition = Acquisition('foo', produce, consumers=[consumer])
    # Now we can run the acquisition
    acquisition()

.. autoclass:: concert.experiments.base.Acquisition
    :members:


Base
----

Base :class:`.base.Experiment` makes sure all acquisitions are executed. It also
holds :class:`.addons.Addon` instances which provide some extra functionality,
e.g. live preview, online reconstruction, etc. To make a simple experiment for
running the acquisition above and storing log with
:class:`concert.storage.Walker`::

    import logging
    from concert.experiments.base import Acquisition, Experiment
    from concert.storage import DirectoryWalker

    LOG = logging.getLogger(__name__)

    walker = DirectoryWalker(log=LOG)
    acquisitions = [Acquisition('foo', produce)]
    experiment = Experiment(acquisitions, walker)

    future = experiment.run()

.. autoclass:: concert.experiments.base.Experiment
    :members:

Experiments also have a :py:attr:`.base.Experiment.log` attribute, which gets a
new handler on every experiment run and this handler stores the output in the
current experiment working directory defined by it's
:class:`concert.storage.Walker`.

Advanced
--------

Sometimes we need finer control over when exactly is the data acquired and worry
about the download later. We can use the *acquire* argument to
:class:`~.base.Acquisition`. This means that the data acquisition can be invoked
independently from the processing stage. By default, the
:class:`~.base.Acquisition` calls its *acquire* and then connects the processing
immediately. To use the separate acquisition we may e.g. reimplement the
:meth:`.base.Experiment.acquire` method::

    class SplitExperiment(Experiment):

        def acquire(self):
            # Here we acquire
            for acq in self.acquisitions:
                acq.acquire()

            # Do something in between
            pass

            # Here we process
            for acq in self.acquisitions:
                acq.connect()


Imaging
-------

A basic frame acquisition generator which triggers the camera itself is provided by
:func:`.frames`

.. autofunction:: concert.experiments.imaging.frames

There are tomography helper functions which make it easier to define the proper
settings for conducting a tomographic experiment.

.. autofunction:: concert.experiments.imaging.tomo_angular_step

.. autofunction:: concert.experiments.imaging.tomo_projections_number

.. autofunction:: concert.experiments.imaging.tomo_max_speed


Control
-------

.. automodule:: concert.experiments.control
    :members:

Addons
------

Addons are special features which are attached to experiments and operate on
their data acquisition. For example, to save images on disk::

    from concert.experiments.addons import ImageWriter

    # Let's assume an experiment is already defined
    writer = ImageWriter(experiment.acquisitions, experiment.walker)
    writer.attach()
    # Now images are written on disk
    experiment.run()
    # To remove the writing addon
    writer.detach()

.. automodule:: concert.experiments.addons
    :members:
