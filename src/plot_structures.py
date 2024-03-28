import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.ticker import AutoMinorLocator


path_figures = '../figures'


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
        str_color = 'lawngreen'
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
    fig = plt.figure(figsize=(4, 8))
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

        ax.text(0, cur_thickness_lower + (max_height - cur_thickness_lower) / 2 / 2, get_label_material(material),
            ha='center', va='center', fontsize=16)

        cur_thickness_lower += thickness

    ax.set_xlim([-grid_size / 2, grid_size / 2])
#    ax.set_ylim([-max_height / 2 + thickness_total / 2, max_height / 2 + thickness_total / 2])
    ax.set_ylim([0, max_height / 2 + thickness_total / 2])

#    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.tick_params(axis='both', which='major', labelsize=16)

    ax.tick_params(which='major', direction='out', length=8)
    ax.tick_params(which='minor', direction='out', length=4)

    ax.get_xaxis().set_visible(False)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)

    fontsize_label = 24
    ax2.set_xlabel(r'$x$ \textrm{(nm)}', fontsize=fontsize_label)
    ax2.set_ylabel(r'$z$ \textrm{(nm)}', fontsize=fontsize_label)

    ax2.invert_yaxis()
    plt.tight_layout()

    if save_figure:
        plt.savefig(os.path.join(path_all, f'{str_figure}.pdf'),
            format='pdf', transparent=True, bbox_inches='tight')
        plt.savefig(os.path.join(path_all, f'{str_figure}.png'),
            format='png', transparent=True, bbox_inches='tight')

    if show_figure:
        plt.show()
    plt.close('all')
