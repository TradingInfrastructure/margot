# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from margot.data.frames import MargotDataFrame
from margot.data.symbols import Symbol
from margot.data.ratio import Ratio
from margot.data.column import alphavantage, cboe
from margot.data.features import finance
from margot.signals.algos import BaseAlgo
from margot.signals.backtest import BackTest
from margot.signals import Position


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

