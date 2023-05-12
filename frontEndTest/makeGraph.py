import matplotlib.pyplot as plt
import numpy as np


def generate_plot(x_data, y_data):
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    return fig
