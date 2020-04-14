import matplotlib
import matplotlib.pyplot as plt
import numpy as np



font = {'family' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)



pc_3 = (4.5, 5.1, 23.2, 406)
pc_2 = (13.7, 15.5, 232, 719)
dev = (6.9, 9.4, 31.2, 2379)
rasp = (23.5, 28.1, 287, 3387)

full = np.arange(len(dev))  # the x locations for the groups
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(full - width * 1.5, pc_3, width, label='Desktop PC + USB 3.0 Accelerator')
rects2 = ax.bar(full - width * 0.5, dev, width, label='Coral Dev Board')
rects3 = ax.bar(full + width * 0.5, pc_2, width, label='Desktop PC + USB 2.0 Accelerator')
rects4 = ax.bar(full + width * 1.5, rasp, width, label='Raspberry pi 3b + USB 2.0 Accelerator')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_yscale('log')
ax.set_ylabel('Inference time (ms)')
ax.set_xticks(full)
ax.set_xticklabels(('Mobilenet V1', 'Mobilenet V2', 'Inception', 'Resnet'))
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
autolabel(rects4, "center")

fig.tight_layout()

plt.show()