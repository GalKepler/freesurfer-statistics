========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/freesurfer_stats/badge/?style=flat
    :target: https://freesurfer_stats.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/GalBenZvi/freesurfer_stats/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/GalBenZvi/freesurfer_stats/actions

.. |requires| image:: https://requires.io/github/GalBenZvi/freesurfer_stats/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/GalBenZvi/freesurfer_stats/requirements/?branch=main

.. |codecov| image:: https://codecov.io/gh/GalBenZvi/freesurfer_stats/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/GalBenZvi/freesurfer_stats

.. |version| image:: https://img.shields.io/pypi/v/freesurfer-statistics.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/freesurfer-statistics

.. |wheel| image:: https://img.shields.io/pypi/wheel/freesurfer-statistics.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/freesurfer-statistics

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/freesurfer-statistics.svg
    :alt: Supported versions
    :target: https://pypi.org/project/freesurfer-statistics

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/freesurfer-statistics.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/freesurfer-statistics

.. |commits-since| image:: https://img.shields.io/github/commits-since/GalBenZvi/freesurfer_stats/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/GalBenZvi/freesurfer_stats/compare/v0.0.0...main



.. end-badges

A Python package for conviniently parsing Freesurfer-derived stats files.

* Free software: Apache Software License 2.0

About The Project
==================
`Freesurfer`_ is an open source neuroimaging toolkit for processing, analyzing, and visualizing human brain MR images.
Although widely used, some of the most popular tools for analyzing (specifically structural) datasets are relatively not user-friendly.
An example for such tool is the cortical and sub-cortical parcellations conducted during the structural processing;

The freesurfer_stats package is a Python package for parsing Freesurfer's .stats files, which are the result of the above-mentioned parcellations.
These files are custom-made for the Freesurfer software, and can be somewhat difficult to query.

.. _Freesurfer: https://surfer.nmr.mgh.harvard.edu/

Features
=========

* Parsing of .stats files' "metadata", i.e headers located in these files, describing the process leading to their making:
* Parsing of .stats files' columns' properties, i.e. the columns' names, their types, and their values:
* Extracting whole-brain metrics and measurements from cortical parcellations.
* Extracting all available metrics calculated per parcellation scheme's ROI.

Installation
============

::

    pip install freesurfer-statistics

You can also install the in-development version with::

    pip install https://github.com/GalBenZvi/freesurfer_stats/archive/main.zip


Usage
======
Parsing of file's "metadata" -> headers and available metrics

.. code-block:: python3
        
            >>> from freesurfer_stats.cortical_stats import CorticalStats
            >>> stats = CorticalStats('/path/to/stats/file')
            >>> type(stats.headers) # Headers -> "metadata"
            dict
            >>> type(stats.table_columns) # Available measurements extracted per ROI
            pandas.core.frame.DataFrame

Extraction of whole-brain measurements

.. code-block:: python3
        
            >>> from freesurfer_stats.cortical_stats import CorticalStats
            >>> stats = CorticalStats('/path/to/stats/file')
            >>> type(stats.whole_brain_measurements)
            pandas.core.frame.DataFrame


Documentation
=============


https://freesurfer_stats.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
