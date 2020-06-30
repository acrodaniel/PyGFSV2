

# GFS Reforecast V2 Grib File Downloader

This is a small package to download version 2 reforecasts
from the global forecast system (GFS). The data can be accessed
via the NOAA CDC data server (National Oceanographic and Atmospheric Agency).
The package provides a handy way to access and download a specific subset
across all reforecasts.

The **GFSV2** python package provides a set of functions and two executables
called ``GFSV2_get`` and ``GFSV2_bulk`` for convenient data processing.

Some more details about the most recent changes can be found in the
[CHANGELOG.md](CHANGELOG.md) file.

## Update (I blamed my script but it was the the HDD)

For those who came across this package in September 2017: I've written a
warning that there are some unknown problems. Everyhing looks fine! The
problem was caused by the hard drive where my scripts were running. Due to
serious segfaults the downloader crashed relatively randomly *arrr*.

While (trying to) bucktrack this issue I've added some additional settings in
the  `curl` section in the config files (optional), see [lisa.conf](lisa.conf)
or [config/default.conf](config/default.conf) files, section `curl`.
Furthermore, an overall sleep time (see section `[main] sleeptime` has been
added (optional).  These options should help to avoid getting blacklisted if
several dozens of requests are made. However, as the rules are unknown
(`ftp.cdc.noaa.gov`) you might see what works for you (depending on internet
speed, number of requests, ...).

* `[curl] curllog`: string, logfile. If given, pycurl drops some download logs there.
* `[curl] timeout`: integer. Custom pycurl timeout.
* `[curl] retries`: integer. `0` (only one shot), else number of retries if download fails.
* `[curl] sleeptime`: time in seconds to sleep if download failed (before try to download again,
   only has an effect if `retries > 0`).
* `[main] sleeptime`: time in seconds to sleep after each download (each file which has to be
   downloaded; not the time to wait between two retries).

## Installation

The [github](https://github.com/retostauffer/PyGFSV2]) repository contains the
small python package which should be ready for installation. You can simply
install the package by calling:

* `pip install git+https://github.com/retostauffer/PyGFSV2.git`

The `setup.py` script should automatically take care of the dependencies
except `wgrib2` which is used for subsetting (if configuration files with subset
settings are used in `GFSV2_bulk`; see below). After installation you can try
the installation (no subsetting) by calling:

* `python GFSV2_get.py --step 12 24 --level 700 850 --param tmp_pres --date 2005-01-01`


## Requirements

Requires the following python packages:
* ``pycurl`` (and standard libs like ``datetime``, ``ConfigParser``, ``argparse``,``logging``)
* If subsetting is used (see ``GFSV2_bulk``) the ``wgrib2`` executable has to be callable
   ([see CPC wgrib2 readme](http://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/)).

## GFSV2_get executable:

The ``GFSV2_get`` executable can be used to download specific manually defined
subsets of the reforecast. This can be handy during the development/specification
process. However, if you would like to download larger amounts of data please
have a look at the ``GFSV2_bulk`` description below!

Basic usage (shows usage help):
* ``GFSV2_get`` or ``GFSV2_get -h``

There are two required input arguments to ``GFSV2_get``. One is the ``-p/--param``
input, the other one is the ``-d/--date`` input. Both can contain one or more
values. ``--param`` specifies which parameters or variables you would like to
download, ``--date`` the dates of the model initialization. A list/description
of [all available parameters can be found here](https://www.esrl.noaa.gov/psd/forecasts/reforecast2/README.GEFS_Reforecast2.pdf).
The ``--date`` arguments have to be of type ``YYYY-mm-dd``. As an example
let's download ``tmax_2m`` for January 1 2014:
* ``GFSV2_get --param tmax_2m --date 2014-01-01``
* ``GFSV2_get -p tmax_2m -d 2014-01-01``

In addition, a ``-s/--steps`` argument can be given. The ``steps`` are the
forecast lead times (e.g., ``24`` for the forecast 24 hours after initialization).
Several steps can be defined:
* ``GFSV2_get -p tmax_2m -d 2014-02-01 -s 24 48``

By default only ``mean`` and ``sprd`` files (ensemble mean and ensemble spread)
will be downloaded. If the individual members and the control run are required
(``10+1``) the ``-m/--members`` flag has to be set:
* ``GFSV2_get -p tmax_2m -d 2014-02-05 -s 24 -m``

Downloading two different parameters for two different dates, only +24h forecast:
* ``GFSV2_get -p tmax_2m cape_sfc -d 2014-02-01 2014-02-02 -s 24

For pressure level variables (e.g, ``ugrd_pres``, ``vgrd_pres``, ``tmp_pres``, ``hgt_pres`` and ``spfh_pres``
([see here, Table 1](https://www.esrl.noaa.gov/psd/forecasts/reforecast2/README.GEFS_Reforecast2.pdf)) the 
level can be given in advance to download specific levels only. Level specification
in millibars or hecto pascal. An example:
* ``GFSV2_get -p tmp_pres -l 500 -d 2014-03-10``

**NOTE:** The download will be skipped if the output grib file already exists!
This can be crucial if you download a data set, re-specify the settings and try
to run the script again. As the file already exists (even if containing different
subset of data) the data won't be downloaded again. In this case simply delete
the local grib files in ``data/YYYY/mm`` and re-run the job.

## GFSV2_bulk executable

This is the bulk download version of the ``GFSV2_get`` executable explained
above. Rather than providing a set of input arguments only one argument is
allowed and required: ``-c/--config``. ``-c/--config`` is the path to a config
file. All specifications can be set in this config file. The config file allows
to specify:

* Specific ouptut path/file name.
* Date range for which data should be downloaded (``from`` ``to``).
* Additional ``only`` flag (download data for date range if and only if the
   date is in month ``only``) .
* The ``steps`` to download.
* A spatial subset (required ``wgrib2`` installed). Data will be subsetted after 
   downloading with respect to the specification (``lonmin``, ``lonmax``, ``latmin`` and ``latmax``).
* Parameters which have to be downloaded (each one can have it's own level/members specification).

The default config file (used by ``GFSV2_get``) can
[be found here](GFSV2/config/default.conf) and can be used as a template
to specify the data set you need. A second template config can be found
in the repository called [lisa.conf](lisa.conf). After you have made a copy
and changed the config specification simply call:

* ``GFSV2_bulk --config your_config_file.conf``







