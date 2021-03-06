Zorg Drivers for Grove
======================

For full documentation visit `zorg-grove.readthedocs.org`_.

Contents:
---------

.. toctree::
   :maxdepth: 2

   docs/LCD
   docs/microphone
   docs/rotary-angle-sensor
   docs/servo
   docs/temperature-sensor

Overview
--------

This package includes python drivers for controling hardware devices.
Typically, this package will not be used directly. The normal useage
would be to include it as a device driver when configuring a robot using
`Zorg`_.

Installation
------------

Install this package using

::

    pip install zorg-grove

Usage
-----

The driver should be included using the dot-notated format of the import
string.

::

    "zorg_grove.Servo"

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _zorg-grove.readthedocs.org: http://zorg-grove.readthedocs.org/
.. _Zorg: http://zorg.github.io/
