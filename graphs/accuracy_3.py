import matplotlib
import matplotlib.pyplot as plt
import numpy as np



font = {'family' : 'normal',
        'size'   : 24}

matplotlib.rc('font', **font)

voc = (45.11, 45.15, 41.02, 42.51)
detrac = (64.27, 66.76, 66.83, 68.43)
dev = (78.52, 81.39, 79.42, 82.51)

full = np.arange(len(dev))  # the x locations for the groups
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(full - width, voc, width, label='PASCAL VOC')
rects2 = ax.bar(full, detrac, width, label='DETRAC')
rects3 = ax.bar(full + width, dev, width, label='Testing custom')

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_yscale('log')
ax.set_ylabel('Car + Truck AP(0.5)')
ax.set_xticks(full)
ax.set_xticklabels(('Mobilenet V2-7(300)', 'Mobilenet V2-7(360)', 'Mobilenet V2-7(420)', 'Mobilenet V2-7(540)'))

locs = ["upper left", "lower left", "center right"]
ax.legend(loc = locs[0], bbox_to_anchor=(0.184,1.1))


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