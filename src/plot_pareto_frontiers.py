import numpy as np
import os
import matplotlib.pyplot as plt


path_results = '../results'
path_figures = '../figures'

num_layerss = [2, 4, 6, 8]
seeds = np.arange(42, 421, 42)
num_init = 10
num_iter = 500


def is_pareto_frontier(objs):
    assert isinstance(objs, np.ndarray)
    assert len(objs.shape) == 2
    assert objs.shape[1] == 2

    is_pareto = np.ones(objs.shape[0], dtype=bool)

    for i, c in enumerate(objs):
        if is_pareto[i]:
            is_pareto[is_pareto] = np.any(objs[is_pareto] > c, axis=1)
            is_pareto[i] = True
    return is_pareto

def plot(Y, num_layers):
    plt.rc('text', usetex=True)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.gca()
    cm = plt.get_cmap('tab10')

    pareto_frontier = Y[is_pareto_frontier(Y)]
    indices = np.argsort(pareto_frontier[:, 0])
    pareto_frontier = pareto_frontier[indices]

    ax.plot(Y[:, 0], Y[:, 1], linestyle='none', color=cm(2), marker='.', markersize=14)
    ax.plot(pareto_frontier[:, 0], pareto_frontier[:, 1], linestyle='solid', linewidth=4, color=cm(3))

    ax.set_xlabel(r'\textrm{Transmittance}', fontsize=24)
    ax.set_ylabel(r'\textrm{Shielding Effectiveness (dB)}', fontsize=24)

    plt.tick_params(axis='both', which='major', labelsize=20)

    plt.grid()
    plt.tight_layout()

    if save_figure:
        plt.savefig(os.path.join(path_figures, f'pareto_layers_{num_layers}.pdf'), format='pdf', transparent=True, bbox_inches='tight')
        plt.savefig(os.path.join(path_figures, f'pareto_layers_{num_layers}.png'), format='png', transparent=True, bbox_inches='tight')

    if show_figure:
        plt.show()

    plt.close('all')


if __name__ == '__main__':
    show_figure = True
    save_figure = False

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

            transparencies_all += list(transparencies)
            shielding_effectivenesses_all += list(shielding_effectivenesses)

        Y = np.array([transparencies_all, shielding_effectivenesses_all]).T
        print(Y.shape)

        plot(Y, num_layers)
