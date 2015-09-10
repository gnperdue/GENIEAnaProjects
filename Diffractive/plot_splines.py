#!/usr/bin/env python
'''
Open a GENIE spline file with formatting circa 2.9.N.
Usage:
    python plot_splines.py <-f>/<-flag> <arg>
                           -c / --cm2         : Plot cross seciton in cm^{2}
                           -s / --splines spline1,spline2,spline3,...

'''
from __future__ import print_function
from xml.etree import ElementTree as ET
import subprocess

meter = 5.07e+15  # 5.07e+15 / GeV
centimeter = 0.01 * meter
cm2 = centimeter * centimeter
global p_has_dvipng


def decode_flavor(flavor):
    """
    Change the PDG code into a string.
    """
    return {
        '-16': 'Tau Antineutrino',
        '-14': 'Muon Antineutrino',
        '-12': 'Electron Antineutrino',
        '12': 'Electron Neutrino',
        '14': 'Muon Neutrino',
        '16': 'Tau Neutrino'
    }.get(flavor, 'Unknown')


def decode_target(targetcode):
    """
    Change the PDG ion code into a named string. Growing into this...
    """
    return {
        '1000010010': 'Hydrogen',
        '1000060120': 'Carbon',
        '1000080160': 'Oxygen'
    }.get(targetcode, 'PDG Ion Code: ' + targetcode)


def decode_nc_cc(proc):
    """
    Figure out whether a proc is CC or NC.
    """
    import re
    cc_pat = re.compile(r"\[CC\]")
    nc_pat = re.compile(r"\[NC\]")
    if cc_pat.search(proc):
        return 'CC'
    if nc_pat.search(proc):
        return 'NC'
    return 'Unknown Current'


def get_neutrino_description(description):
    """
    Take a GENIE description string like:
        'genie::ReinSeghalCOHPiPXSec/Default/nu:-14;tgt:1000060120;
         proc:Weak[CC],COH;hmult:(p=0,n=0,pi+=0,pi-=1,pi0=0);'
    and return:
    {'algorithm': 'ReinSeghalCOHPiPXSec',
     'flavor': 'Muon Antineutrino',
     'hmult': '(p=0,n=0,pi+=0,pi-=1,pi0=0)',
     'proc': 'Weak[CC],COH',
     'tgt': '1000060120'}
    """
    components = description.split(';')
    alg_flavor = components[0].split('/')
    alg = alg_flavor[0].split(':')[-1]
    flavor = decode_flavor(alg_flavor[-1].split(':')[-1])
    ddict = {'algorithm': alg, 'flavor': flavor}
    components = components[1:]
    for component in components:
        elem = component.split(':')
        if len(elem) > 1:
            ddict[elem[0]] = elem[1]

    return ddict


def process_spline(spline):
    """
    Transform a spline (object) from an ElementTree retrieval
    into a dictionary containing the relevant information.
    """
    knots = spline.findall('./knot')
    xsecs = []
    for knot in knots:
        e = knot.find('./E')
        x = knot.find('./xsec')
        en = float(e.text)
        xs = float(x.text)
        xsecs.append((en, xs))
    description = get_neutrino_description(spline.get('name'))
    return {'description': description, 'xsecs': xsecs}


def xml_to_list_of_dicts(xml_file_name):
    """
    Take an xml file and return a list of dictionaries, where each dictionary
    contains a description and a list of tuples for energy and cross section.
    The description key is 'description' and the cross sections key is 'xsecs'.
    """
    xsec_xml = ET.parse(xml_file_name)
    splines = xsec_xml.findall('./spline')
    neutrino_xsecs = []

    for spline in splines:
        xsec_dict = process_spline(spline)
        neutrino_xsecs.append(xsec_dict)

    return neutrino_xsecs


def get_xyaxis_titles_total_xsec(plot_cm2):
    y_axis_title = r''
    if p_has_dvipng:
        y_axis_title = r'Cross Section (per GeV$^{-2}$)'
        if plot_cm2:
            y_axis_title = r'Cross Section (per $10^{-39}$ cm$^{2}$)'
    else:
        y_axis_title = r'Cross Section (per GeV^(-2))'
        if plot_cm2:
            y_axis_title = r'Cross Section (per 10^(-39) cm^2)'

    x_axis_title = r'Neutrino Energy (GeV)'

    return (x_axis_title, y_axis_title)


def plot_xsec_dict(xsd, plot_cm2):
    import matplotlib.pyplot as plt
    import re

    global p_has_dvipng
    plt.clf()
    plt.ioff()
    plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
    if p_has_dvipng:
        plt.rc('text', usetex=True)

    title = xsd['description']['algorithm'] + " " + \
        xsd['description']['flavor'] + " " +\
        decode_nc_cc(xsd['description']['proc']) + \
        " on " + decode_target(xsd['description']['tgt'])
    file_name = re.sub(r'\s+', '_', title)

    x_axis_title, y_axis_title = get_xyaxis_titles_total_xsec(plot_cm2)

    xsecs_tup = xsd['xsecs']
    energies = []
    xsecs = []
    for tup in xsecs_tup:
        energies.append(tup[0])
        xsecs.append(tup[1] / cm2 / 1e-39 if plot_cm2 else tup[1])

    plt.plot(energies, xsecs)
    plt.xlabel(x_axis_title)
    plt.ylabel(y_axis_title)
    plt.title(title)
    plt.savefig(file_name + ".pdf")


def plot_data_and_xsec_dict(xsd, filenam):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.lines as mlines
    import re

    global p_has_dvipng
    plt.clf()
    plt.ioff()
    plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
    if p_has_dvipng:
        plt.rc('text', usetex=True)

    cf = pd.read_csv(filenam,
                     skiprows=[0, 1, 2, 3, 4, 5],
                     names=['Bin Center', 'Cross Section', 'Bin Low',
                            'Bin High', 'Unc. Low', 'Unc. High'])
    cf['Cross Section'] = cf['Cross Section'] / 1e-39
    cf['Unc. High'] = cf['Unc. High'] / 1e-39
    cf['Unc. Low'] = cf['Unc. Low'] / 1e-39
    cf['Uncertainty'] = (cf['Unc. High'] - cf['Unc. Low']) / 2.0
    cf['Bin Width'] = (cf['Bin High'] - cf['Bin Low']) / 2.0
    cf.plot(x='Bin Center', y='Cross Section',
            xerr='Bin Width', yerr='Uncertainty',
            kind='scatter', color='black')

    title = xsd['description']['algorithm'] + " " + \
        xsd['description']['flavor'] + " " +\
        decode_nc_cc(xsd['description']['proc']) + \
        " on " + decode_target(xsd['description']['tgt'])

    print(title)

    xsecs_tup = xsd['xsecs']
    energies = []
    xsecs = []
    for tup in xsecs_tup:
        energies.append(tup[0])
        xsecs.append(tup[1] / cm2 / 1e-39)

    x_axis_title, y_axis_title = get_xyaxis_titles_total_xsec(True)

    plt.plot(energies, xsecs, color='red')
    plt.xlabel(x_axis_title)
    plt.ylabel(y_axis_title)
    plt.xlim([0, 105])
    plt.ylim([0, 5])
    plt.title(title)

    red_line = mlines.Line2D([], [], color='red', label='GENIE 2.8.6')
    black_pts = mlines.Line2D([], [], color='black', marker='o',
                              linestyle='None', label='BEBC Data')
    plt.legend(handles=[red_line, black_pts], numpoints=1, loc=0)

    file_name = re.sub(r'\s+', '_', title)
    plt.savefig(file_name + ".pdf")


def spline_list_split(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage=__doc__)
    parser.add_option('-c', '--cm2', dest='plot_cm2', default=False,
                      help=r'Plot in cm^{2}', action='store_true')
    parser.add_option('-s', '--splines', type='string', action='callback',
                      callback=spline_list_split, dest='spline_files')
    (options, args) = parser.parse_args()

    global p_has_dvipng
    p_has_dvipng = False
    p = subprocess.Popen(["which", "dvipng"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    (dvipng_out, dvipng_err) = p.communicate()
    if len(dvipng_err) == 0:
        p_has_dvipng = True

    list_of_dicts = []
    for spline_file in options.spline_files:
        list_of_dicts.extend(xml_to_list_of_dicts(spline_file))

    nu_d = {}
    anu_d = {}
    for d in list_of_dicts:
        print(d['description'])
        if d['description']['flavor'] == 'Muon Neutrino' and \
                decode_nc_cc(d['description']['proc']) == 'CC':
            nu_d = d.copy()
        if d['description']['flavor'] == 'Muon Antineutrino' and \
                decode_nc_cc(d['description']['proc']) == 'CC':
            anu_d = d.copy()

    plot_data_and_xsec_dict(nu_d, "./bebc_neutrino_data.csv")
    plot_data_and_xsec_dict(anu_d, "./bebc_antineutrino_data.csv")
