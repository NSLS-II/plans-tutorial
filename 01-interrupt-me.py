from bluesky.plans import count
from bluesky import RunEngine
from bluesky.examples import det
from bluesky.callbacks import LiveTable

RE = RunEngine({})
RE(count([det], num=None, delay=0.3), LiveTable([det]))
