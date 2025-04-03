import argparse
import numpy as np
from textwrap import wrap

MAX_TITLE_LENGTH = 65


def plot_freq_response(lognames, calibration_data, max_freq, recommend_shaper_idx):
    freqs = calibration_data.freq_bins
    # We don't know if "psd" from the csv means X+Y+Z
    # or the sole axis that we are calibrating for. Probably the former.
    psd = calibration_data.psd_sum[freqs <= max_freq]
    freqs = freqs[freqs <= max_freq]

    fontP = matplotlib.font_manager.FontProperties()
    fontP.set_size('x-small')

    fig, ax = matplotlib.pyplot.subplots()
    ax.set_xlabel('Frequency, Hz')
    ax.set_xlim([0, max_freq])
    ax.set_ylabel('Power spectral density')

    ax.plot(freqs, psd, label='psd', color='purple')

    title = "Frequency response and shapers (%s)" % (', '.join(lognames))
    ax.set_title("\n".join(wrap(title, MAX_TITLE_LENGTH)))
    ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax.grid(which='major', color='grey')
    ax.grid(which='minor', color='lightgrey')

    ax2 = ax.twinx()
    ax2.set_ylabel('Shaper vibration reduction (ratio)')
    best_shaper_vals = None

    for i in range(len(calibration_data.shaper_names)):
        shaper_name = calibration_data.shaper_names[i]
        label = calibration_data.labels[i]

        linestyle = 'dotted'
        if i == recommend_shaper_idx:
            linestyle = 'dashdot'
            best_shaper_vals = calibration_data.data[shaper_name]
        ax2.plot(freqs, calibration_data.data[shaper_name], label=label, linestyle=linestyle)
    ax.plot(freqs, psd * best_shaper_vals,
            label='After\nshaper', color='cyan')
    # A hack to add a human-readable shaper recommendation to legend
    ax2.plot([], [], ' ',
             label="Recommended shaper: %s" % (calibration_data.shaper_names[recommend_shaper_idx].upper()))

    ax.legend(loc='upper left', prop=fontP)
    ax2.legend(loc='upper right', prop=fontP)

    fig.tight_layout()
    return fig


def plot_after_shapers(lognames, calibration_data, max_freq, recommend_shaper_idx):
    freqs = calibration_data.freq_bins
    # We don't know if "psd" from the csv means X+Y+Z
    # or the sole axis that we are calibrating for. Probably the former.
    psd = calibration_data.psd_sum[freqs <= max_freq]

    freqs = freqs[freqs <= max_freq]

    fontP = matplotlib.font_manager.FontProperties()
    fontP.set_size('x-small')

    fig, ax = matplotlib.pyplot.subplots()
    ax.set_xlabel('Frequency, Hz')
    ax.set_xlim([0, max_freq])
    ax.set_ylabel('Power spectral density')

    title = "Estimated response after shapers (%s)" % (', '.join(lognames))
    ax.set_title("\n".join(wrap(title, MAX_TITLE_LENGTH)))
    ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax.grid(which='major', color='grey')
    ax.grid(which='minor', color='lightgrey')

    for i in range(len(calibration_data.shaper_names)):
        shaper_name = calibration_data.shaper_names[i]
        label = calibration_data.labels[i]
        color = None
        if i == recommend_shaper_idx:
            color = 'cyan'
        ax.plot(freqs, psd * calibration_data.data[shaper_name], label=label, color=color)

    # A hack to add a human-readable shaper recommendation to legend
    ax.plot([], [], ' ',
            label="Recommended shaper: %s" % (calibration_data.shaper_names[recommend_shaper_idx].upper()))

    ax.legend(prop=fontP)

    fig.tight_layout()
    return fig


class CalibrationData:
    def __init__(self, data, labels):
        names = data.dtype.names
        self.freq_bins = data[names[0]]
        self.psd_sum = data[names[1]]
        self.data = data
        self.shaper_names = names[2:]
        self.labels = labels


def setup_matplotlib(output_to_file):
    global matplotlib
    if output_to_file:
        matplotlib.rcParams.update({'figure.autolayout': True})
        matplotlib.use('Agg')
    import matplotlib.pyplot, matplotlib.dates, matplotlib.font_manager
    import matplotlib.ticker


def read_csv(filename):
    data = np.genfromtxt(filename, dtype=None, delimiter=',', names=True)
    labels = []
    new_names = []
    for name in data.dtype.names:
        if 'i' in name:
            s = name.find("i")
        elif 'v' in name:
            s = name.find("v")
        else:
            s = None

        if s is not None:
            label = f'{name[:s + 1]} ({int(name[s + 1:]) / 10} Hz)'
            labels.append(label)
            new_names.append(name[:s + 1])
        else:
            new_names.append(name)

    data.dtype.names = tuple(new_names)

    calibration_data = CalibrationData(data, labels)
    return calibration_data


def visualize_shaper_calibration(filename, recommended_shaper_idx, is_plotting_extra, is_freq_lim_200hz):
    calibration_data = read_csv(filename)

    if is_freq_lim_200hz:
        max_freq = 200
    else:
        max_freq = calibration_data.freq_bins[-1]

    setup_matplotlib(None)
    fig = plot_freq_response([filename], calibration_data, max_freq, recommended_shaper_idx)
    if is_plotting_extra:
        fig2 = plot_after_shapers([filename], calibration_data, max_freq, recommended_shaper_idx)
    matplotlib.pyplot.show()  # TODO replace with fig.show? It disappears instantly


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Path to a CSV calibration file to visualize.')
    parser.add_argument('recommended_shaper_idx', help='An integer (0 to 4), '
                                                       'selects corresponding shaper (zv to 3hump_ei) '
                                                       'as recommended to highlight it on the plots.', type=int)
    parser.add_argument('-e', '--extra', help='Plot extra graph for applied shapers estimation.', action="store_true")
    parser.add_argument('-f', '--fixed_lims', help='Fix frequency range to 0-200Hz, otherwise '
                                                   'set range according to data.', action="store_true")

    args = parser.parse_args()

    visualize_shaper_calibration(args.filename, args.recommended_shaper_idx, args.extra, args.fixed_lims)





