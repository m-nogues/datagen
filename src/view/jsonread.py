import json

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter


def _scale_data(data, ranges):
    return data


def set_rgrids(self, radii, labels=None, angle=None, fmt=None, **kwargs):
    """
    Set the radial locations and labels of the *r* grids.
    The labels will appear at radial distances *radii* at the
    given *angle* in degrees.
    *labels*, if not None, is a ``len(radii)`` list of strings of the
    labels to use at each radius.
    If *labels* is None, the built-in formatter will be used.
    Return value is a list of tuples (*line*, *label*), where
    *line* is :class:`~matplotlib.lines.Line2D` instances and the
    *label* is :class:`~matplotlib.text.Text` instances.
    kwargs are optional text properties for the labels:
    %(Text)s
    ACCEPTS: sequence of floats
    """
    # Make sure we take into account unitized data
    radii = self.convert_xunits(radii)
    radii = np.asarray(radii)
    # if rmin <= 0:
    #     raise ValueError('radial grids must be strictly positive')

    self.set_yticks(radii)
    if labels is not None:
        self.set_yticklabels(labels)
    elif fmt is not None:
        self.yaxis.set_major_formatter(FormatStrFormatter(fmt))
    if angle is None:
        angle = self.get_rlabel_position()
    self.set_rlabel_position(angle)
    for t in self.yaxis.get_ticklabels():
        t.update(kwargs)
    return self.yaxis.get_gridlines(), self.yaxis.get_ticklabels()


def json_report(indi, file_name):
    class ComplexRadar:
        def __init__(self, fig, variables, ranges,
                     n_ordinate_levels=6):
            angles = np.arange(0, 360, 360. / len(variables))

            axes = [fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True,
                                 label="axes{}".format(i)) for i in range(len(variables))]
            l, text = axes[0].set_thetagrids(angles, labels=variables)
            [text.set_rotation(angles - 90) for text, angle
             in zip(text, angles)]
            for ax in axes[1:]:
                ax.patch.set_visible(False)
                ax.grid("off")
                ax.xaxis.set_visible(False)
            for i, ax in enumerate(axes):
                grid = np.linspace(*ranges[i], num=n_ordinate_levels)
                gridlabel = ["{}".format(round(x, 2)) for x in grid]
                if ranges[i][0] > ranges[i][1]:
                    grid = grid[::-1]  # hack to invert grid
                    # gridlabels aren't reversed
                gridlabel[0] = ""  # clean up origin
                # ax.set_rgrids(grid, labels=gridlabel, angle=angles[i])
                set_rgrids(ax, grid, labels=gridlabel, angle=angles[i])
                # ax.spines["polar"].set_visible(False)
                ax.set_ylim(*ranges[i])
            # variables for plotting
            self.angle = np.deg2rad(np.r_[angles, angles[0]])
            self.ranges = ranges
            self.ax = axes[0]

        def plot(self, data, *args, **kw):
            sdata = _scale_data(data, self.ranges)
            self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

        def fill(self, data, *args, **kw):
            sdata = _scale_data(data, self.ranges)
            self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

    variables = (' ips', ' response_avg', 'ports', '1st_quartile', 'variance en s',)
    data = [indi['ips'], indi['response_avg'], len(indi['ports']), indi['ip_life']['1st_quartile'],
            float(indi['ip_life']['variance'])]
    ranges = [(0, 2000), (0, 4), (0, 1000), (0, 3), (0, 2 * float(indi['ip_life']['variance']))]
    # l'échelle depend pour beaucoup des donnés ici elle est assez grande pour les gros fichier de plusieurs Go

    fig1 = plt.figure(figsize=(6, 6))
    radar = ComplexRadar(fig1, variables, ranges)
    radar.plot(data)
    radar.fill(data, alpha=0.2)
    plt.savefig(file_name + '/pdf/radar-chart.pdf', facecolor='white')
