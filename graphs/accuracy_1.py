import matplotlib
import matplotlib.pyplot as plt
import numpy as np


font = {'family' : 'normal',
        'size'   : 20}

matplotlib.rc('font', **font)


voc = (39.33, 43.80, 31.43, 45.67)
detrac = (43.1, 66.86, 32.84, 65.05)
dev = (48.64, 81.75, 41.88, 78.54)

full = np.arange(len(dev))  # the x locations for the groups
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(full - width, voc, width, label='PASCAL VOC')
rects2 = ax.bar(full, detrac, width, label='DETRAC')
rects3 = ax.bar(full + width, dev, width, label='Testing custom')

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_yscale('log')
ax.set_ylabel('Car AP(0.5)')
ax.set_xticks(full)
ax.set_xticklabels(('Mobilenet V1', 'Retrained Mobilenet V1', 'Mobilenet V2', 'Retrained Mobilenet V2'))
ax.legend()


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