#!/usr/bin/env python3

import setuptools


setuptools.setup(
    name='odessacubex',
    version='0.1',
    py_modules=['config_aware', 'cube_api', 'telegram_bot', 'website'],
    packages=['cubex'],
    entry_points={},
        # Note, any changes to your setup.py, like adding to `packages`, or
        # changing `entry_points` will require the module to be reinstalled;
        # `python3 -m pip install --upgrade --editable ./folder
)
