import matplotlib
import matplotlib.pyplot as plt
import numpy as np



import numpy as np
import scipy.stats


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


font = {'family' : 'normal',
        'size'   : 20}

matplotlib.rc('font', **font)



v1_retrained_dev_data = mean_confidence_interval([86.45, 87.58, 86.37, 85.86, 84.61])
v1_retrained_detrac_data = mean_confidence_interval([66.48, 67.12, 67.45, 67.18, 65.89])
v1_retrained_voc_data = mean_confidence_interval([43.59, 42.20, 40.41, 41.44, 41.27])


v2_retrained_dev_data = mean_confidence_interval([83.32, 85.61, 83.88, 82.23, 82.77])
v2_retrained_detrac_data =mean_confidence_interval([65.57, 67.93, 64.64, 64.30, 65.75])
v2_retrained_voc_data = mean_confidence_interval([45.91, 45.70, 42.00, 45.64, 44.47])



voc = (39.33, v1_retrained_voc_data[0], 31.43, v2_retrained_voc_data[0])
detrac = (43.1, v1_retrained_detrac_data[0], 32.84, v2_retrained_detrac_data[0])
dev = (53.7, v1_retrained_dev_data[0], 45.6, v2_retrained_dev_data[0])


dev = [round(i, 1) for i in dev]
detrac = [round(i, 1) for i in detrac]
voc = [round(i, 1) for i in voc]


full = np.arange(len(dev))  # the x locations for the groups
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(full - width, voc, width, label='PASCAL VOC', yerr=[0, v1_retrained_voc_data[2] - v1_retrained_voc_data[1], 0, v2_retrained_voc_data[2] - v2_retrained_voc_data[1]], capsize=7)
rects2 = ax.bar(full, detrac, width, label='DETRAC', yerr=[0, v1_retrained_detrac_data[2] - v1_retrained_detrac_data[1], 0, v2_retrained_detrac_data[2] - v2_retrained_detrac_data[1]], capsize=7)
rects3 = ax.bar(full + width, dev, width, label='Training custom', yerr=[0, v1_retrained_dev_data[2] - v1_retrained_dev_data[1], 0, v2_retrained_dev_data[2] - v2_retrained_dev_data[1]], capsize=7, color='brown')

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_yscale('log')
ax.set_ylabel('Car AP(0.5)')
ax.set_xticks(full)
ax.set_xticklabels(('Mobilenet V1(300)', 'Retrained Mobilenet V1-6(300)', 'Mobilenet V2(300)', 'Retrained Mobilenet V2-6(300)'))
ax.legend()


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for i, rect in enumerate(rects):
        height = rect.get_height()

        if i % 2 == 1:
            #ax.annotate('{}'.format(height),  xy=(rect.get_x() + rect.get_width() / 2, height),  xytext=(-50, -10), textcoords="offset points", ha=ha[xpos], va='bottom')
            ax.annotate('{}'.format(height),  xy=(rect.get_x() + rect.get_width() / 2, height),  xytext=(-3*2, 2), textcoords="offset points", ha=ha['left'], va='bottom')
        else:
            ax.annotate('{}'.format(height),  xy=(rect.get_x() + rect.get_width() / 2, height),  xytext=(offset[xpos]*2, 2), textcoords="offset points", ha=ha[xpos], va='bottom')


autolabel(rects1, "center")
autolabel(rects2, "center")
autolabel(rects3, "center")

fig.tight_layout()

plt.show()
