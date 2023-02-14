from xyplot.Set import SetAxes, SetFigure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from pprint import pprint
import matplotlib as mpl
#
# print(mpl.rcParams)
# exit()
# mpl.rcParams['text.color'] = 'w'


def read_data(file):
    with open(file, 'r') as f:
        line_list = list(filter(lambda x: x[0] != '#', f.readlines()))
    variables = line_list[1].strip().split("=")[1].replace('"', '').split(",")
    data_list = []
    for line in line_list[6:]:
        try:
            line_data = [float(i) for i in line.strip().split(" ") if i]
        except:
            continue
        data_list.append(line_data)

    return pd.DataFrame(columns=variables, data=data_list)


file = r"P-L1-IMM-SWMF_20221018004619_0005M_SWMF.dat"
df = read_data(file)
# print(df.keys())
x, y = df['X [R]'], df['Y [R]']
xx = yy = np.linspace(-6.5, 6.5, 1000)
X, Y = np.meshgrid(xx, yy)
grid_data = griddata((x, y), df[df.keys()[7]].values, (X, Y), method="linear")  # 散点插值成网格数据
U = griddata((x, y), df[df.keys()[8]].values, (X, Y), method="linear")  # 散点插值成网格数据
V = griddata((x, y), df[df.keys()[9]].values, (X, Y), method="linear")  # 散点插值成网格数据

x = np.linspace(-np.pi, np.pi, 100)
y = np.sin(x)
cfg = dict(
    title=dict(args="SIN(X)", loc='left'),
    xlabel=dict(args="x label", c='k'),
    ylabel=dict(args=r'$\sin(x)$', c='k'),
    legend=dict(
        loc='upper right',
    ),
    annotate=dict(
        text='Hello',
        xy=(0.3, 0.3),
        xytext=(0.5, 0.5),
        weight='bold',
        color='b',
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='b')
    ),
    grid=dict(linestyle=':', color='r'),
    text=(
        dict(args=(-3.0, 0.0, "TEXT"), weight='bold', color='r', fontsize=20, fontfamily='sans-serif'),
        dict(args=(0.5, 0., "text"), weight='bold', color='g', fontsize=20, fontfamily='sans-serif'),
    ),
    axhline=dict(y=0, c='g', ls='--', lw=2),
    axvline=dict(x=0, c='c', ls='-.', lw=2),
    axvspan=dict(xmin=1.0, xmax=2.0, facecolor='y', alpha=0.1),
    axhspan=dict(ymin=0.1, ymax=0.4, facecolor='r', alpha=0.1),
    plot=dict(args=(x, y), label=r'$y = \sin(x)$', c='k'),
    scatter=dict(args=([0, 1, -3, ], [.4, -.7, -.9]), label='scatter', color='r'),
    streamplot=dict(args=(X, Y, grid_data, grid_data), density=1.5, linewidth=0.5, arrowsize=0.9, arrowstyle='->'),
    set_aspect=True,
    branch=dict(
        contourf=dict(
            contourf=dict(args=(X, Y, grid_data),
                          levels=np.linspace(0, 30, 50),
                          cmap='hot',),
            cbar=dict(
                shrink=0.8,
                ticks=np.linspace(0, 30, 11),
                ax=dict(
                    title=dict(
                        args='title',
                        c='y'
                    ),
                    xlabel='123',
                    ylabel='EEE',
                )
            )
        ),
        patches=dict(
            wedge=(
                dict(center=(0, 0), r=1, theta1=90, theta2=270, color='k',),
                dict(center=(0, 0), r=1, theta1=-90, theta2=90, edgecolor='k', facecolor='w'),
            )
        ),
        axis=dict(
            spines=dict(
                top=dict(
                    set_position=dict(args=(('data', 0), )),
                    set_color='b',

                )
            ),
            xaxis=dict(
                set_label_coords=dict(args=(1, -0.05), ),
                set_tick_params=dict(color='b'),
            )
        )
    )
)

fig_dit = dict(
    height=10, width=10, facecolor='w', edgecolor='r',
    legend=dict(
        loc='upper right'
    ),
    frameon=True,
    branch=dict(
    )
)

fig = plt.figure()
ax = fig.add_axes(plt.axes())
import time
t = time.time()
SetAxes(ax, **cfg)
SetFigure(fig, **fig_dit)

# ax1 = fig.add_axes(polar=True)
# cset = ax.contourf(X, Y, grid_data, cmap='hot', levels=np.linspace(0, 30, 100),)
# cbar = fig.colorbar(cset, shrink=0.8,)
print(time.time() - t)
# pprint(fig.__dict__)
plt.show()