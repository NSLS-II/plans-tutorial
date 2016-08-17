import matplotlib.pyplot as plt

from bluesky.plan_tools import plot_raster_path

from bluesky.examples import motor1, motor2, det

from bluesky.plans import outer_product_scan

plan = outer_product_scan([det], motor1, -5, 5, 10, motor2, -7, 7, 15, True)

fig, ax = plt.subplots()
plot_raster_path(plan, 'motor1', 'motor2', probe_size=.3, ax=ax)
plt.show()
