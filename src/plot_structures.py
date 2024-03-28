import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.ticker import AutoMinorLocator

import plot_pareto_frontiers as ppf


path_results = '../results'
path_figures = '../figures'

num_layerss = [2, 4, 6, 8]
seeds = np.arange(42, 421, 42)
num_init = 10
num_iter = 500


def get_color(material):
    if material == 'Ag':
        str_color = 'silver'
    elif material == 'Al':
        str_color = 'yellow'
    elif material == 'Ni':
        str_color = 'olive'
    elif material == 'Cr':
        str_color = 'red'
    elif material == 'Ti':
        str_color = 'turquoise'
    elif material == 'W':
        str_color = 'orange'
    elif material == 'TiO2':
        str_color = 'blue'
    elif material == 'TiN':
        str_color = 'darkgreen'
    elif material == 'Al2O3':
        str_color = 'magenta'
    elif material == 'SiO2':
        str_color = 'brown'
    elif material == 'Si3N4':
        str_color = 'lightpink'
    elif material == 'Pd':
        str_color = 'slategray'
    else:
        print(material)
        raise ValueError

    return str_color

def convert_to_latex_expression(material):
    return r'\textrm{' + material + r'}'

def get_label_material(material):
    if material == 'TiO2':
        str_label = r'\textrm{TiO}$_2$'
    elif material == 'Al2O3':
        str_label = r'\textrm{Al}$_2$\textrm{O}$_3$'
    elif material == 'SiO2':
        str_label = r'\textrm{SiO}$_2$'
    elif material == 'Si3N4':
        str_label = r'\textrm{Si}$_3$\textrm{N}$_4$'
    else:
        str_label = convert_to_latex_expression(material)

    return str_label

def plot_structure(materials, thicknesses, show_figure, save_figure, str_figure):
    grid_size = 100

    plt.rc('text', usetex=True)
    fig = plt.figure(figsize=(6, 8))
    ax = fig.gca()

    thickness_total = np.sum(thicknesses)
    max_height = thickness_total * 1.25

    cur_thickness_lower = 0.0
    for material, thickness in zip(materials, thicknesses):
        assert cur_thickness_lower >= 0
        assert thickness > 0

        points = np.array([
            [grid_size / 2, cur_thickness_lower + thickness],
            [-grid_size / 2, cur_thickness_lower + thickness],
            [-grid_size / 2, cur_thickness_lower],
            [grid_size / 2, cur_thickness_lower],
        ])
        color = get_color(material)

        polygon = Polygon(points, facecolor=color)
        ax.add_patch(polygon)

        ax.text(0, cur_thickness_lower + thickness / 2, get_label_material(material),
            ha='center', va='center', fontsize=22)

        cur_thickness_lower += thickness

    ax.set_xlim([-grid_size / 2, grid_size / 2])
    ax.set_ylim([-max_height / 2 + thickness_total / 2, max_height / 2 + thickness_total / 2])

    ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.tick_params(axis='both', which='major', labelsize=22)

    ax.tick_params(which='major', direction='out', length=8)
    ax.tick_params(which='minor', direction='out', length=4)

    ax.get_xaxis().set_visible(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    fontsize_label = 28
    ax.set_ylabel(r'\textrm{Thickness (nm)}', fontsize=fontsize_label)

    plt.tight_layout()

    if save_figure:
        plt.savefig(os.path.join(path_all, f'{str_figure}.pdf'),
            format='pdf', transparent=True, bbox_inches='tight')
        plt.savefig(os.path.join(path_all, f'{str_figure}.png'),
            format='png', transparent=True, bbox_inches='tight')

    if show_figure:
        plt.show()

    plt.close('all')

if __name__ == '__main__':
    show_figure = True
    save_figure = False

    for num_layers in num_layerss:
        materials_all = []
        thicknesses_all = []
        transparencies_all = []
        shielding_effectivenesses_all = []

        for seed in seeds:
            str_file = f'mobo_layers_{num_layers}_init_{num_init}_iter_{num_iter}_seed_{seed:04d}.npy'

            results = np.load(os.path.join(path_results, str_file), allow_pickle=True)
            results = results[()]

            materials = results['materials']
            thicknesses = results['thicknesses']

            negative_transparencies = results['negative_transparencies']
            negative_shielding_effectivenesses = results['negative_shielding_effectivenesses']

            transparencies = -1.0 * negative_transparencies
            shielding_effectivenesses = -1.0 * negative_shielding_effectivenesses

            materials_all += list(materials)
            thicknesses_all += list(thicknesses)
            transparencies_all += list(transparencies)
            shielding_effectivenesses_all += list(shielding_effectivenesses)

        materials_all = np.array(materials_all)
        thicknesses_all = np.array(thicknesses_all)
        Y = np.array([transparencies_all, shielding_effectivenesses_all]).T
        print(materials_all.shape)
        print(thicknesses_all.shape)
        print(Y.shape)

        is_pf = ppf.is_pareto_frontier(Y)

        materials_all = materials_all[is_pf]
        thicknesses_all = thicknesses_all[is_pf]
        pareto_frontier = Y[is_pf]
        print(materials_all.shape)
        print(thicknesses_all.shape)
        print(pareto_frontier.shape)

        indices = []
        for ind, pareto in enumerate(pareto_frontier):
            if pareto[0] >= 0.65 and pareto[1] >= 30:
                indices.append(ind)
        print(len(indices))

        for ind, elem in enumerate(zip(materials_all, thicknesses_all)):
            materials, thicknesses = elem
            str_figure = f'structure_layers_{num_layers}_{ind + 1:03d}'

            plot_structure(materials, thicknesses, show_figure, save_figure, str_figure)
