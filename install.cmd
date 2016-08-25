@echo off
@rem Get the Python 3.5 installer for miniconda.
@rem http://conda.pydata.org/miniconda.html

@rem Then open a terminal / command prompt and type or paste this:

conda create --name plans-demo python=3.5 ipython matplotlib scipy
activate plans-demo
pip install boltons prettytable
pip install http://github.com/NSLS-II/event-model/zipball/v1.1.0
pip install http://github.com/NSLS-II/bluesky/zipball/v0.6.3
pip install http://github.com/NSLS-II/doct/zipball/v1.0.2
