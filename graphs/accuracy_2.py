import matplotlib
import matplotlib.pyplot as plt
import numpy as np



font = {'family' : 'normal',
        'size'   : 20}

matplotlib.rc('font', **font)

voc = (55.85, 32.80, 52.15, 49.25)
detrac = (27.44, 48.41, 21.79, 40.97)
dev = (13.64, 54.45, 10.50, 55.78)

full = np.arange(len(dev))  # the x locations for the groups
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(full - width, voc, width, label='PASCAL VOC')
rects2 = ax.bar(full, detrac, width, label='DETRAC')
rects3 = ax.bar(full + width, dev, width, label='Testing custom')

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_yscale('log')
ax.set_ylabel('Truck AP(0.5)')
ax.set_xticks(full)
ax.set_xticklabels(('Mobilenet V1', 'Retrained Mobilenet V1', 'Mobilenet V2', 'Retrained Mobilenet V2'))

locs = ["upper left", "lower left", "center right"]
ax.legend(loc = locs[0], bbox_to_anchor=(0.2,1.0))


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*2, 2),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


autolabel(rects1, "center")
autolabel(rects2, "center")
autolabel(rects3, "center")

fig.tight_layout()

plt.show()