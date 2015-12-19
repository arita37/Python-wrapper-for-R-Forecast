Python wrapper for R Forecast
=============================

*This is work in progress.*

This project uses rpy2 to expose most of the functionality of R's Forecast package in python. 
Some related functions in the stats and base packages are also exposed (e.g. seasonal decompositions).
A few less-commnonly used functions and arguments are not exposed.

An example of generating a forecast:

.. code-block:: python

   from rforecast import wrappers  
   from rforecast import ts_io  
  
   stock = ts_io.read_series('data/livestock.csv')  
   fc = wrappers.forecast(stock)  
   print fc  

This example uses the ``livestock`` series in ``data/`` under the installation directory.

An example of generating an STL decomposition:

.. code-block:: python

   aus = ts_io.read_series('aus.csv')  
   dc = wrappers.stl(aus, s_window=5)  
   print dc  


The rforecast.py package uses Pandas Series objects to represent time series.
For seasonal series, it uses a multindex with the second level of the index
denoting the season. The ``read_series`` function in ``ts_io`` will return a 
series with the index constructed correctly. 
If the data are already in a Python sequence, such as a list or numpy array,
you can convert it to a series of the right form like this:

.. code-block:: python

   from rforecast import converters  
   # A slice of the 'oil' data from R package fpp, available in data/  
   data =  [509, 506, 340, 240, 219, 172, 252, 221, 276, 271, 342, 428, 442, 432, 437]  
   ts = converters.sequence_as_series(data, start=1980)  
   print ts
   
   # A seasonal (quarterly) series:
   data = [30.05, 19.14, 25.31, 27.59, 32.07, 23.48, 28.47, 35.12, 
           36.83, 25.00, 30.72, 28.69, 36.64, 23.82, 29.31, 31.77]
   ts = converters.sequence_as_series(data, start=(1991, 1), freq=4)
   print ts

There is more information in the `.rst` files under ``doc/``. 
The documentation is built with Sphinx. 
If you have Sphinx installed, you can build the documentation using the Makefile 
in ``doc``:

.. code-block:: bash

  cd doc
  make html

Then the built documentation will start at: doc/_build/html/index.html.