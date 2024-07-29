from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def lineplot_timeseries(
    data: list[float],
    dates_data: list[datetime | None],
    fig_size: tuple[int, int] = (10, 6),
    save_path: str | None = None,
    label: str = "",
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    color: str = "blue",
) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(1, 1, figsize=fig_size)
    # ax = subplots[0]
    if any(value is None for value in dates_data):
        ax.plot(data, label=label, color=color)
    else:
        ax.plot(
            dates_data,  # type: ignore
            data,
            label=label,
            color=color,
        )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.grid(True)

    if save_path:
        fig.savefig(save_path)
    else:
        plt.show()

    return fig, ax
