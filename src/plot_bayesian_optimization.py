import numpy as np
import os
import matplotlib.pyplot as plt


path_results = '../results'
path_figures = '../figures'

num_layerss = [2, 4, 6, 8]
seeds = np.arange(42, 421, 42)
num_init = 10
num_iter = 500


def plot(means, sems, num_layers, str_objective, show_figure, save_figure):
    cm = plt.get_cmap('tab10')

    if str_objective == 'trans':
        str_label = r'\textrm{Transmittance}'
        str_ylabel = r'\textrm{Maximum transmittance}'
        color = cm(0)
    elif str_objective == 'effec':
        str_label = r'\textrm{Shielding effectiveness}'
        str_ylabel = r'\textrm{Maximum shielding effectiveness (dB)}'
        color = cm(1)
    else:
        raise ValueError

    plt.rc('text', usetex=True)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.gca()

    bx = np.arange(0, means.shape[0])

    ax.plot(bx, means, label=str_label, linewidth=4, linestyle='solid', color=color)
    ax.fill_between(bx, means - sems, means + sems, alpha=0.3, color=color)

    ax.set_xlabel(r'\textrm{Iteration}', fontsize=24)
    ax.set_ylabel(str_ylabel, fontsize=24)

    ax.set_xlim([0, np.max(bx)])
    plt.tick_params(axis='both', which='major', labelsize=20)

    plt.grid()
    plt.tight_layout()

    if save_figure:
        plt.savefig(os.path.join(path_figures, f'maxima_layers_{num_layers}_{str_objective}.pdf'),
            format='pdf', transparent=True, bbox_inches='tight')
        plt.savefig(os.path.join(path_figures, f'maxima_layers_{num_layers}_{str_objective}.png'),
            format='png', transparent=True, bbox_inches='tight')

    if show_figure:
        plt.show()

    plt.close('all')

def get_maxima(values, num_init):
    new_values = []

    for value in values:
        new_value = [np.max(value[:num_init])]

        for val in value[num_init:]:
            if new_value[-1] < val:
                new_value.append(val)
            else:
                new_value.append(new_value[-1])
        new_values.append(new_value)
    return np.array(new_values)

def get_means_sems(values):
    means = np.mean(values, axis=0)
    sems = np.std(values, axis=0, ddof=1) / np.sqrt(values.shape[0])
    return means, sems


if __name__ == '__main__':
    show_figure = True
    save_figure = True

    for num_layers in num_layerss:
        transparencies_all = []
        shielding_effectivenesses_all = []

        for seed in seeds:
            str_file = f'mobo_layers_{num_layers}_init_{num_init}_iter_{num_iter}_seed_{seed:04d}.npy'

            results = np.load(os.path.join(path_results, str_file), allow_pickle=True)
            results = results[()]

            negative_transparencies = results['negative_transparencies']
            negative_shielding_effectivenesses = results['negative_shielding_effectivenesses']

            transparencies = -1.0 * negative_transparencies
            shielding_effectivenesses = -1.0 * negative_shielding_effectivenesses

            print(transparencies.shape)
            print(shielding_effectivenesses.shape)

            transparencies_all.append(transparencies)
            shielding_effectivenesses_all.append(shielding_effectivenesses)

        trans = get_maxima(transparencies_all, num_init)
        effec = get_maxima(shielding_effectivenesses_all, num_init)

        means_trans, sems_trans = get_means_sems(trans)
        means_effec, sems_effec = get_means_sems(effec)

        plot(means_trans, sems_trans, num_layers, 'trans', show_figure, save_figure)
        plot(means_effec, sems_effec, num_layers, 'effec', show_figure, save_figure)
