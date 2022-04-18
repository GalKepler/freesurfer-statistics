================
Freesurfer Stats
================


.. image:: https://img.shields.io/pypi/v/freesurfer_stats.svg
        :target: https://pypi.python.org/pypi/freesurfer_stats

.. image:: https://img.shields.io/travis/GalBenZvi/freesurfer_stats.svg
        :target: https://travis-ci.com/GalBenZvi/freesurfer_stats

.. image:: https://readthedocs.org/projects/freesurfer-stats/badge/?version=latest
        :target: https://freesurfer-stats.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Python package for conviniently parsing Freesurfer's .stats files.


* Free software: Apache Software License 2.0
* Documentation: https://freesurfer-stats.readthedocs.io.

About The Project
--------
`Freesurfer`_ is an open source neuroimaging toolkit for processing, analyzing, and visualizing human brain MR images.
Although widely used, some of the most popular tools for analyzing (specifically structural) datasets are relatively not user-friendly.
An example for such tool is the cortical and sub-cortical parcellations conducted during the structural processing;

The freesurfer_stats package is a Python package for parsing Freesurfer's .stats files, which are the result of the above-mentioned parcellations.
These files are custom-made for the Freesurfer software, and can be somewhat difficult to query.

.. _Freesurfer: https://surfer.nmr.mgh.harvard.edu/

Features
--------

* Parsing of .stats files' "metadata", i.e headers located in these files, describing the process leading to their making:
* Parsing of .stats files' columns' properties, i.e. the columns' names, their types, and their values:
* Extracting whole-brain metrics and measurements from cortical parcellations.
* Extracting all available metrics calculated per parcellation scheme's ROI.

Usage
--------
Parsing of file's "metadata" -> headers and available metrics

.. code-block:: python
        
            >>> from freesurfer_stats.cortical_stats import CorticalStats
            >>> stats = CorticalStats('/path/to/stats/file')
            >>> type(stats.headers) # Headers -> "metadata"
            dict
            >>> type(stats.table_columns) # Available measurements extracted per ROI
            pandas.core.frame.DataFrame
  
Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
