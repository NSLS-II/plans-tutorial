from bluesky import RunEngine
from bluesky.examples import motor, det, Mover
from bluesky.spec_api import ascan
from bluesky.global_state import gs
from bluesky.utils import install_qt_kicker


INSTALL = True
if INSTALL:
    install_qt_kicker()
    INSTALL = False

RE = RunEngine({'proposal_id': 'test'})

det.exposure_time = .3
sample_plate = Mover('sample', ['sample'])

gs.BASELINE_DEVICES = [sample_plate]
gs.DETS = [det]
gs.PLOT_Y = 'det'

sample_list = ['a', 'b', 'c']
sample_ranges = {'a': {'start': -5, 'finish': -1},
                 'b': {'start': -1, 'finish': 1},
                 'c': {'start': 1, 'finish': 5}}


def sample_plan(sample_list):
    for sample in sample_list:
        s_range = sample_ranges[sample]
        yield from ascan(motor, intervals=10, md={'sample': sample}, **s_range)
