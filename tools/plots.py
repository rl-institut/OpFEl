import numpy as np
import matplotlib.pyplot as plt


def plot_bar_horizontal(series, x_labels, figsize=(3.5, 2.5), title='',
                        max_val=None, save_fig_dir=None, label_name='',
                        no_label=False, **kwargs):
    """
    Horizontal bar plot for visualisation of parameter distribution.

    :param series:  pandas.Series with values that should be displayed
    :param x_labels:    list of labels of bars, can either be of same length of
                        series, then one bar is plotted or double the length,
                        then two overlaying bars are plotted
    :param figsize: tuple (optional)
    :param title:   string (optional)
    :param max_val: float (optional), maximum value of examined parameter,
                    normally number of models in ordner to plot percentage of
                    models that have implemented the examined parameters
    :param save_fig_dir: string (optional)
    :param label_name:  string, defaults to '', then 'possible' and 'usually
                        used' are used as labels, for 'pos_def' the labels
                        'possible' and 'defined' are used and for 'yes_no'
                        'yes' and 'no' serve as labels
    :param no_label:    bool, if True legend is not displayed
    """
    plt.ion()
    fig, ax = plt.subplots(figsize=figsize)
    x_pos = np.arange(len(x_labels))
    y_values = series.values/max_val * 100
    plt.title(title)
    if not no_label:
        plt.xlabel('Share of models [%]', horizontalalignment='right', x=1.0)
    else:
        plt.xlabel('Share of models [%]', x=0.5)
    if len(x_pos) == len(y_values):
        plt.barh(x_pos, y_values[x_pos], align='center')
        no_label = True
    elif label_name == '':
        plt.barh(x_pos, y_values[x_pos*2], align='center', label='possible')
        plt.barh(
            x_pos, y_values[x_pos*2+1], align='center', label='usually\nused')
    elif label_name == 'pos_def':
        plt.barh(x_pos, y_values[x_pos*2], align='center', label='possible')
        plt.barh(x_pos, y_values[x_pos*2+1], align='center', label='defined')
    elif label_name == 'yes_no':
        plt.barh(x_pos, y_values[x_pos * 2], align='center', label='yes')
        plt.barh(x_pos, y_values[x_pos * 2 + 1], align='center', label='no')
    elif label_name == 'no_yes':
        plt.barh(x_pos, y_values[x_pos * 2 + 1], align='center', label='no')
        plt.barh(x_pos, y_values[x_pos * 2], align='center', label='yes')
    ax.set_yticks(range(len(x_labels)))
    ax.set_yticklabels(x_labels, rotation='horizontal')
    ax.invert_yaxis()
    if max_val is not None:
        plt.xlim(0, 100)
    plt.subplots_adjust(left=0.2)
    if not no_label:
        legend_location = kwargs.get('legend_location', 'upper center')
        bbox_to_anchor = kwargs.get('bbox_to_anchor', (1, 0.43))
        plt.legend(loc=legend_location, bbox_to_anchor=bbox_to_anchor,#(1.3, 1)
                   fancybox=True, shadow=True, ncol=1)
    plt.tight_layout()
    if save_fig_dir is not None:
        fig.savefig(save_fig_dir)


def plot_representation_triple(rating, parameters_1, parameters_2,
                               subtitle_1=None, subtitle_2=None, title=None,
                               figsize=(6.5, 4.8), save_fig_dir=None):
    """
    Method for heat map plot of relative representation of two groups of
    different parameters in selected models with rating on the left.

    :param rating:  pandas.DataFrame, index should be the model names, should
                    only include one column
    :param parameters_1:    pandas.DataFrame, index should be the model names
                            and columns the evaluated parameters
    :param parameters_2:    pandas.DataFrame, index should be the model names
                            and columns the evaluated parameters
    :param subtitle_1:  string (optional), name of parameter group left
    :param subtitle_2:  string (optional), name of parameter group right
    :param title:   string (optional)
    :param figsize: tuple (optional)
    :param save_fig_dir:    string (optional), complete path to which figure
                            should be saved
    """
    plt.ion()
    fig, (ax0, ax, ax2) = plt.subplots(1, 3, gridspec_kw={
        'width_ratios': [0.5, 3, 3.75]},
                                       figsize=figsize)
    im0 = ax0.imshow(rating, cmap="YlGn", aspect='auto', vmin=0, vmax=1)
    im = ax.imshow(parameters_1, cmap="YlGn", aspect='auto', vmin=0, vmax=1)
    plt.subplots_adjust(wspace=None, hspace=None)
    im2 = ax2.imshow(parameters_2, cmap="YlGn", aspect='auto', vmin=0, vmax=1)
    plt.subplots_adjust(wspace=None, hspace=None)
    # set colorbar and adjust size of second subplot
    cbar = ax2.figure.colorbar(im, ax=ax2)
    cbar.mappable.set_clim(0, 1.0)
    cbar.ax.set_ylabel("Level of Representation", rotation=90, va="top")

    # We want to show all ticks...
    ax0.set_xticks(np.arange(rating.shape[1]))
    ax.set_xticks(np.arange(parameters_1.shape[1]))
    ax2.set_xticks(np.arange(parameters_2.shape[1]))
    ax0.set_yticks(np.arange(parameters_1.shape[0]))
    ax.set_yticks([])
    ax2.set_yticks([])
    # ... and label them with the respective list entries.
    ax0.set_xticklabels(rating.columns, rotation='vertical')
    ax.set_xticklabels(parameters_1.columns, rotation='vertical')
    ax2.set_xticklabels(parameters_2.columns, rotation='vertical')
    ax0.set_yticklabels(parameters_1.index)
    plt.subplots_adjust(bottom=0.15)
    # set title
    if subtitle_1 is not None:
        ax.set_title(subtitle_1)
    if subtitle_2 is not None:
        ax2.set_title(subtitle_2)
    plt.subplots_adjust(left=0, wspace=0)
    if title is not None:
        fig.suptitle(title)
    plt.tight_layout()
    if save_fig_dir is not None:
        plt.savefig(save_fig_dir)


def plot_representation_dual(parameters_1, parameters_2,
                             subtitle_1=None, subtitle_2=None, title=None,
                             figsize=(6.5, 4.8), save_fig_dir=None):
    """
    Method for heat map plot of relative representation of two groups of
    different parameters in selected models without rating on the left.


    :param parameters_1:    pandas.DataFrame, index should be the model names
                            and columns the evaluated parameters
    :param parameters_2:    pandas.DataFrame, index should be the model names
                            and columns the evaluated parameters
    :param subtitle_1:  string (optional), name of parameter group left
    :param subtitle_2:  string (optional), name of parameter group right
    :param title:   string (optional)
    :param figsize: tuple (optional)
    :param save_fig_dir:    string (optional), complete path to which figure
                            should be saved
    """
    plt.ion()
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=figsize)
    im = ax.imshow(parameters_1, cmap="YlGn", aspect='auto', vmin=0, vmax=1)
    plt.subplots_adjust(wspace=None, hspace=None)
    im2 = ax2.imshow(parameters_2, cmap="YlGn", aspect='auto', vmin=0, vmax=1)
    plt.subplots_adjust(wspace=None, hspace=None)
    # set colorbar and adjust size of second subplot
    cbar = ax2.figure.colorbar(im, ax=ax2)
    cbar.mappable.set_clim(0, 1.0)
    cbar.ax.set_ylabel("Level of Representation", rotation=90, va="top")
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider2 = make_axes_locatable(ax)
    cax2 = divider2.append_axes("right", size="5%", pad=0.35)
    cax2.axis('off')
    # We want to show all ticks...
    ax.set_xticks(np.arange(parameters_1.shape[1]))
    ax2.set_xticks(np.arange(parameters_2.shape[1]))
    ax.set_yticks(np.arange(parameters_1.shape[0]))
    ax2.set_yticks([])
    # ... and label them with the respective list entries.
    ax.set_xticklabels(parameters_1.columns, rotation='vertical')
    ax2.set_xticklabels(parameters_2.columns, rotation='vertical')
    ax.set_yticklabels(parameters_1.index)
    plt.subplots_adjust(bottom=0.15)
    # set title
    if subtitle_1 is not None:
        ax.set_title(subtitle_1)
    if subtitle_2 is not None:
        ax2.set_title(subtitle_2)
    plt.subplots_adjust(left=0.2, wspace=0)
    if title is not None:
        fig.suptitle(title)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    if save_fig_dir is not None:
        plt.savefig(save_fig_dir)


def plot_representation_single(parameters, title=None,
                               save_fig_dir=None, figsize=(6.5, 4.8)):
    """
    Method for heat map plot of relative representation of
    different parameters in selected models without rating on the left.


    :param parameters:    pandas.DataFrame, index should be the model names
                            and columns the evaluated parameters
    :param title:   string (optional)
    :param figsize: tuple (optional)
    :param save_fig_dir:    string (optional), complete path to which figure
                            should be saved
    """
    plt.ion()
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    im = ax.imshow(parameters, cmap="YlGn", aspect='auto', vmin=0, vmax=1)
    # set colorbar and adjust size of second subplot
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.mappable.set_clim(0, 1.0)
    cbar.ax.set_ylabel("Level of Representation", rotation=90, va="top")
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    # We want to show all ticks...
    ax.set_xticks(np.arange(parameters.shape[1]))
    ax.set_yticks(np.arange(parameters.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(parameters.columns, rotation='vertical')
    ax.set_yticklabels(parameters.index)
    plt.subplots_adjust(bottom=0.19)
    # set title
    if title is not None:
        ax.set_title(title)
    plt.subplots_adjust(left=0.2, wspace=0)
    plt.tight_layout()
    if save_fig_dir is not None:
        plt.savefig(save_fig_dir)


def plot_representation_holistic(rating, parameters, title=None,
                                 save_fig_dir=None, figsize=(6.5, 4.8)):
    """
    Method for heat map plot of relative representation of
    different parameters in selected models with rating on the left.

    :param rating:  pandas.DataFrame, index should be the model names, should
                    only include one column
    :param parameters:      pandas.DataFrame, index should be the model names
                            and columns the evaluated parameters
    :param title:   string (optional)
    :param figsize: tuple (optional)
    :param save_fig_dir:    string (optional), complete path to which figure
                            should be saved
    """
    plt.ion()
    fig, (ax0, ax) = plt.subplots(1, 2,gridspec_kw={
        'width_ratios': [0.5, 6.75]}, figsize=figsize)
    im0 = ax0.imshow(rating, cmap="YlGn", aspect='auto', vmin=0, vmax=1)
    im = ax.imshow(parameters, cmap="YlGn", aspect='auto', vmin=0, vmax=1)
    # set colorbar and adjust size of second subplot
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.mappable.set_clim(0, 1.0)
    cbar.ax.set_ylabel("Level of Representation", rotation=90, va="top")
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    # We want to show all ticks...
    ax0.set_xticks(np.arange(rating.shape[1]))
    ax.set_xticks(np.arange(parameters.shape[1]))
    ax0.set_yticks(np.arange(rating.shape[0]))
    ax.set_yticks([])
    # ... and label them with the respective list entries.
    ax0.set_xticklabels(rating.columns, rotation='vertical')
    ax.set_xticklabels(parameters.columns, rotation='vertical')
    ax0.set_yticklabels(parameters.index)
    ax.set_yticklabels([])
    plt.subplots_adjust(bottom=0.19)
    # set title
    if title is not None:
        ax.set_title(title)
    plt.tight_layout()
    if save_fig_dir is not None:
        plt.savefig(save_fig_dir)


def plot_boxplot(df, save_fig=None):
    """
    Plot box plot of representation of different groups of parameters

    :param df: pandas.DataFrame
    :param save_fig:    string (optional), complete path to which figure
                        should be saved
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title('')
    ax.set_ylim(0, 1)
    bp = ax.boxplot(df, meanline=True, showmeans=True, manage_ticks=True)
    ax.set_xticklabels(df.index, rotation=0)
    ax.legend([bp['medians'][0], bp['means'][0]], ['Median', 'Mean'])
    if save_fig:
        plt.savefig(save_fig)

