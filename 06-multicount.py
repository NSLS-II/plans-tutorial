from bluesky.examples import det1, det2
import bluesky.plans as bp
from bluesky import RunEngine

RE = RunEngine({})

dets = [det1, det2]

# one 'run' with one 'event' (readings for det1 and det2)
RE(bp.count(dets))

# one 'run' with three 'events'
RE(bp.count(dets, num=3))

# If we didn't provide a num option, how could you make one
# yourself?

for _ in range(3):
    RE(bp.count(dets))


def multicount(dets):
    for _ in range(3):
        yield from bp.count(dets)

RE(multicount(dets))


def multicount(dets, num):
    "Creates a separate 'run' for each loop"
    for _ in range(num):
        yield from bp.count(dets)

RE(multicount(dets, 3))


def multicount(dets, num):
    "Creates a single 'run'"
    for det in dets:
        yield from bp.stage(det)
    yield from bp.open_run()
    for _ in range(num):
        yield from bp.trigger_and_read(dets)
    yield from bp.close_run()
    for det in dets:
        yield from bp.unstage(det)


def multicount(dets, num):
    "Adds some metadata specific to this plan"
    md = {'plan_name': 'multicount', 'num': num}
    for det in dets:
        yield from bp.stage(det)
    yield from bp.open_run(md=md)
    for _ in range(num):
        yield from bp.trigger_and_read(dets)
    yield from bp.close_run()
    for det in dets:
        yield from bp.unstage(det)


from collections import ChainMap


def multicount(dets, num, md=None):
    "Allows user to pass in custom metadata."
    if md is None:
        md = {}
    md = ChainMap(md, {'plan_name': 'multicount',
                       'num': num})
    for det in dets:
        yield from bp.stage(det)
    yield from bp.open_run(md=md)
    for _ in range(num):
        yield from bp.trigger_and_read(dets)
    yield from bp.close_run()
    for det in dets:
        yield from bp.unstage(det)
