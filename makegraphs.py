import matplotlib.pyplot as plt
from textwrap import wrap
import matplotlib.font_manager
import time
import json
# Data for plotting

with open('kaiku.json', 'r') as file:
    courses = json.load(file)

for course in courses:
    t = []
    s = []
    w = []
    for instance in course["instances"]:
        t.append(instance["year"])
        s.append(instance["grade"])
        w.append(instance["work"])

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(t, s, '.-', color='#355f8c')
    ax1.set_ylim([2.8, 5])
    ax1.set(xlabel='Year', ylabel='Grade')
    ax1.grid()

    title = ax1.set_title("\n".join(wrap(course["name"], 30)), fontdict={
        'fontfamily': 'Righteous',
        'fontsize': 30,
        'fontweight': 'medium'
    }, y=1.08)

    for i, txt in enumerate(course["instances"]):
        ax1.annotate(txt["grade"], (t[i], s[i]), color='#FFFFFF')

    ax2 = fig.add_subplot(212)

    ax2.set_ylabel('Work')  # we already handled the x-label with ax1
    ax2.plot(t, w, '.-', color='#5f8c35')
    ax2.tick_params(axis='y')
    ax2.set_ylim([-50, 50])
    ax2.grid()

    for i, txt in enumerate(course["instances"]):
        ax2.annotate(txt["work"], (t[i], w[i]), color='#FFFFFF')

    ax1.set_facecolor('#171f28')
    ax1.spines['bottom'].set_color('#FFFFFF')
    ax1.spines['bottom'].set_color('#FFFFFF')
    ax1.spines['top'].set_color('#FFFFFF')
    ax1.spines['right'].set_color('#FFFFFF')
    ax1.spines['left'].set_color('#FFFFFF')
    ax1.tick_params(axis='x', colors='#FFFFFF')
    ax1.tick_params(axis='y', colors='#FFFFFF')
    ax1.yaxis.label.set_color('#FFFFFF')
    ax1.xaxis.label.set_color('#FFFFFF')
    ax1.title.set_color('#FFFFFF')

    ax2.set_facecolor('#171f28')
    ax2.spines['bottom'].set_color('#FFFFFF')
    ax2.spines['bottom'].set_color('#FFFFFF')
    ax2.spines['top'].set_color('#FFFFFF')
    ax2.spines['right'].set_color('#FFFFFF')
    ax2.spines['left'].set_color('#FFFFFF')
    ax2.tick_params(axis='x', colors='#FFFFFF')
    ax2.tick_params(axis='y', colors='#FFFFFF')
    ax2.yaxis.label.set_color('#FFFFFF')
    ax2.xaxis.label.set_color('#FFFFFF')
    ax2.title.set_color('#FFFFFF')

    fig.set_facecolor('#171f28')

    plt.rc('font', size=20)  # controls default text sizes
    plt.rc('axes', titlesize=16)  # fontsize of the axes title
    plt.rc('axes', labelsize=20)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=16)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=16)  # fontsize of the tick labels
    plt.rc('legend', fontsize=20)  # legend fontsize
    plt.rc('figure', titlesize=20)  # fontsize of the figure title

    fig.set_dpi(100)
    fig.set_size_inches(8, 8)
    fig.savefig("site/img/" + course["id"] + ".jpg", bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    # plt.show()
    # time.sleep(1)
    plt.close('all')

