Concert
=======

.. image:: https://badge.fury.io/py/concert.png
    :target: http://badge.fury.io/py/concert

.. image:: https://travis-ci.org/ufo-kit/concert.png?branch=master
    :target: https://travis-ci.org/ufo-kit/concert

.. image:: https://coveralls.io/repos/ufo-kit/concert/badge.png?branch=master
    :target: https://coveralls.io/r/ufo-kit/concert?branch=master

.. image:: https://badge.waffle.io/ufo-kit/concert.png?label=in%20progress&title=In%20Progress
    :target: https://waffle.io/ufo-kit/concert
    :alt: 'Stories in In Progress'

.. image:: https://badge.waffle.io/ufo-kit/concert.png?label=ready&title=Ready
    :target: https://waffle.io/ufo-kit/concert
    :alt: 'Stories in Ready'

*Concert* is a light-weight control system interface to control Tango and native
devices. It can be used as a library::

    from concert.quantities import q
    from concert.devices.motors.dummy import LinearMotor

    motor = LinearMotor()
    motor.position = 10 * q.mm
    motor.move(-5 * q.mm)

or from a session and within an integrated `IPython`_ shell::

    $ concert init session
    $ concert start session

    session > motor.position = 10 * q.mm
    10.0 millimeter

.. _Ipython: http://ipython.org

You can read more about *Concert* in the official `documentation`_.

.. _documentation: https://concert.readthedocs.io/en/latest/


Citation
--------

If you want to use Concert, we kindly ask you to acknowledge the respective
authorship not only by respecting the LGPL software license but also by linking
to our project website at http://ufo.kit.edu and citing the following article:
Vogelgesang, M., Farago, T., Morgeneyer, T. F., Helfen, L., dos Santos Rolo, T.,
Myagotin, A. & Baumbach, T. (2016). J. Synchrotron Rad. 23, 1254-1263,
https://doi.org/10.1107/S1600577516010195.
