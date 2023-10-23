import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

all_cpu_v1 = {}
all_pss_v1 = {}
all_cpu_v2 = {}
all_pss_v2 = {}
ver1 = 2312
ver2 = 2421
titles = [
]


def average(values):
    return sum(values) / len(values)


def read_all_data():
    func_type = []
    for t in func_type:
        file1_cpu, file1_pss = read_data("result_%d_%s.txt" % (ver1, t))
        file2_cpu, file2_pss = read_data("result_%d_%s.txt" % (ver2, t))
        all_cpu_v1[t] = file1_cpu
        all_cpu_v2[t] = file2_cpu
        all_pss_v1[t] = file1_pss
        all_pss_v2[t] = file2_pss


def read_data(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    cpu_values = []
    pss_values = []

    for line in lines:
        if 'completed' in line:
            break
        cpu, pss = line.strip().split(",")[0:2]
        cpu = float(cpu.split(":")[1].strip())
        pss = float(pss.split(":")[1].strip()) / 1024  # Convert to MB
        cpu_values.append(cpu)
        pss_values.append(pss)

    return cpu_values, pss_values


def draw_cpu_8():
    # Create a figure with 8 subplots arranged in a 2x4 grid
    fig, axs = plt.subplots(2, 4, figsize=(15, 6))

    # Loop through the data and create line charts
    for i, title in enumerate(titles):
        # Calculate the row and column index for the current chart
        row = i // 4
        col = i % 4

        # Plot the line chart on the corresponding subplot
        data1 = list(all_cpu_v1[title])
        data2 = list(all_cpu_v2[title])
        axs[row, col].plot(data1, label=ver1)
        axs[row, col].plot(data2, label=ver2)
        axs[row, col].axhline(average(data1), linestyle='--', color='C0', label="%d Average" % ver1)
        axs[row, col].axhline(average(data2), linestyle='--', color='C1', label="%d Average" % ver2)
        axs[row, col].set_title(title)

    fig.suptitle('CPU Usage (%)', fontsize=16)
    legend_elements = [
        Line2D([0], [0], color='C0', lw=2, label=ver1),
        Line2D([0], [0], color='C1', lw=2, label=ver2)
    ]
    fig.legend(handles=legend_elements, loc='upper right', ncol=1, fontsize=12)
    plt.subplots_adjust(hspace=0.5, wspace=0.3, top=0.85)

    plt.savefig("cpu_all.png")
    # Show the figure
    plt.show()


def draw_pss_8():
    # Create a figure with 8 subplots arranged in a 2x4 grid
    fig, axs = plt.subplots(2, 4, figsize=(15, 6))

    # Loop through the data and create line charts
    for i, title in enumerate(titles):
        # Calculate the row and column index for the current chart
        row = i // 4
        col = i % 4

        # Plot the line chart on the corresponding subplot
        data1 = list(all_pss_v1[title])
        data2 = list(all_pss_v2[title])
        axs[row, col].plot(data1, label=ver1)
        axs[row, col].plot(data2, label=ver2)
        axs[row, col].axhline(average(data1), linestyle='--', color='C0')
        axs[row, col].axhline(average(data2), linestyle='--', color='C1')
        axs[row, col].set_title(title)

    fig.suptitle('PSS Values (MB)', fontsize=16)
    legend_elements = [
        Line2D([0], [0], color='C0', lw=2, label=ver1),
        Line2D([0], [0], color='C1', lw=2, label=ver2)
    ]
    fig.legend(handles=legend_elements, loc='upper right', ncol=1, fontsize=12)
    plt.subplots_adjust(hspace=0.5, wspace=0.3, top=0.85)

    plt.savefig("pss_all.png")
    # Show the figure
    plt.show()


def read_time(file_path):
    time_consumed = 0
    with open(file_path, "r") as f:
        lines = f.readlines()
    for i in lines:
        if 'completed' in i:
            time_consumed = i.split(' ')[4]
            break
    return int(time_consumed)


def compare_time(data1, data2):
    if len(data1) != len(data2):
        return
    delta = []
    for i in range(len(data1)):
        oldv = data1[i]
        newv = data2[i]
        print 'oldv=%d,newv=%d'%(oldv,newv)
        delta.append((newv-oldv)*1.0/oldv)
    print '---compare time---'
    print delta
    print average(delta)


def draw_time():
    func_type = []

    task_types = []
    data1 = []
    data2 = []

    for t in func_type:
        task_types.append(t)
        data1.append(read_time("result_%d_%s.txt" % (ver1, t)))
        data2.append(read_time("result_%d_%s.txt" % (ver2, t)))

    print task_types, data1, data2
    compare_time(data1, data2)
    # Calculate the width of each bar and the positions of the bars
    bar_width = 0.35
    indices = np.arange(len(task_types))

    # Draw the bar chart
    fig, ax = plt.subplots(figsize=(15, 6))  # Adjust the width and height as needed

    # Set the y-axis labels and x-axis labels
    ax.set_yticks(indices)
    ax.set_yticklabels(task_types)
    ax.set_ylabel('Task Type')
    ax.set_xlabel('Time (s)')
    ax.legend()
    fig.suptitle('Total Time (%)', fontsize=16)

    plt.savefig('time_consumed.png')
    plt.show()


if __name__ == '__main__':
    # 1.draw CPU and PSS (8 scenarios in one picture)
    read_all_data()
    draw_cpu_8()
    draw_pss_8()
    # 2.draw time comparison
    draw_time()
    # output: [cpu_all.png, pss_all.png, time_consumed.png]
