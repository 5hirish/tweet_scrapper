#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for tweetscrape.

    This file was generated with PyScaffold 3.0.2.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: http://pyscaffold.org/
"""

import sys
import os
import io
from setuptools import setup


def setup_package():

    base_dir = os.path.abspath(os.path.dirname(__file__))
    setup_config = base_dir+'/setup.cfg'
    
    setup(
        setup_cfg=True
    )


if __name__ == "__main__":
    setup_package()