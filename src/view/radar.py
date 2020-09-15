import json
import re
from datetime import timedelta

import numpy as np
import matplotlib
import matplotlib.path as path
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def parse(s):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    return {key: float(val) for key, val in m.groupdict().items()}


def radar_graph(indicators):
    # Data to be represented
    properties = ['ips', 'response_avg', 'ports', '1st_quartile', 'variance en s']
    variance_as_percentage = timedelta(parse(indicators['ip_life']['variance']) / parse(indicators['total_duration']))
    values = [indicators['ips'], indicators['response_avg'], len(indicators['ports']),
              indicators['ip_life']['1st_quartile'], variance_as_percentage]

    # Choose some nice colors
    matplotlib.rc('axes', facecolor='white')

    # Make figure background the same colors as axes
    fig = plt.figure(figsize=(10, 8), facecolor='white')

    # Use a polar axes
    axes = plt.subplot(111, polar=True)

    # Set ticks to the number of properties (in radians)
    t = np.arange(0, 2 * np.pi, 2 * np.pi / len(properties))
    plt.xticks(t, [])

    # Set yticks from 0 to 10
    plt.yticks(np.linspace(0, 10, 11))

    plt.text(-13, 13, str(indicators['exchanges']) + " total exchanges")
    # Draw polygon representing values
    points = [(x, y) for x, y in zip(t, values)]
    points.append(points[0])
    points = np.array(points)
    codes = [path.Path.MOVETO, ] + \
            [path.Path.LINETO, ] * (len(values) - 1) + \
            [path.Path.CLOSEPOLY]
    _path = path.Path(points, codes)
    _patch = patches.PathPatch(_path, fill=True, color='blue', linewidth=0, alpha=.1)
    axes.add_patch(_patch)
    _patch = patches.PathPatch(_path, fill=False, linewidth=2)
    axes.add_patch(_patch)

    # Draw circles at value points
    plt.scatter(points[:, 0], points[:, 1], linewidth=2,
                s=50, color='white', edgecolor='black', zorder=10)

    # Set axes limits
    plt.ylim(0, 10)

    # Draw ytick labels to make sure they fit properly
    for i in range(len(properties)):
        angle_rad = i / float(len(properties)) * 2 * np.pi
        angle_deg = i / float(len(properties)) * 360
        ha = "right"
        if angle_rad < np.pi / 2 or angle_rad > 3 * np.pi / 2: ha = "left"
        # plt.text(angle_rad, 10.75, properties[i], size=14,
        # horizontalalignment=ha, verticalalignment="center")

        # A variant on label orientation
        plt.text(angle_rad, 11, properties[i], size=14, rotation=angle_deg - 90, horizontalalignment='center',
                 verticalalignment="center")

    # Done
    plt.savefig('radar-chart.png', facecolor='white')
    plt.show()
