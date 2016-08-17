# Get the Python 3.5 installer for miniconda.
# http://conda.pydata.org/miniconda.html

# Then open a terminal / command prompt and type or paste this:

conda create --name plans-demo python=3.5 ipython matplotlib
source activate plans-demo
pip install mongoquery
pip install boltons
pip install http://github.com/NSLS-II/portable-mds/zipball/master
pip install http://github.com/NSLS-II/event-model/zipball/v1.1.0
pip install http://github.com/NSLS-II/bluesky/zipball/v0.6.3
