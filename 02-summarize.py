from bluesky.plans import scan, relative_scan
from bluesky import RunEngine
from bluesky.examples import det, motor
from bluesky.callbacks import LiveTable
from bluesky.plan_tools import print_summary

RE = RunEngine({})

print_summary(scan([det], motor, 1, 5, 5))
# print_summary(relative_scan([det], motor, 1, 5, 5))
