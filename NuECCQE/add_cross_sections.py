#!/usr/bin/env python
'''
Open a GENIE spline file with formatting circa 2.9.N.
Usage:
    python add_cross_sections.py <-f>/<-flag> <arg>
                           -s / --splines spline1,spline2,spline3,...
                           -t / --target      : Target (e.g. 1000060120)
                           -n / --min         : Min energy (default 0)
                           -x / --max         : Max energy (default 120 GeV)
                                --nc          : Neutral current (CC default)

Available targets:
    1000010010 (Hydrogen)
    1000060120 (Carbon)
    1000080160 (Oxygen)
'''
from __future__ import print_function
from xml.etree import ElementTree as ET

meter = 5.07e+15  # 5.07e+15 / GeV
centimeter = 0.01 * meter
cm2 = centimeter * centimeter


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


def sum_cross_section_dicts(list_of_dicts):
    """
    Perform a bin by bin summation.
    """
    if len(list_of_dicts) == 1:
        return list_of_dicts[0]['xsecs']
    elif len(list_of_dicts) > 1:
        xsec_sum = list_of_dicts[0]['xsecs']
        [es, xss] = [list(t) for t in zip(*xsec_sum)]
        for d in list_of_dicts[1:]:
            xsecs = d['xsecs']
            [es, xs] = [list(t) for t in zip(*xsecs)]
            for tup in enumerate(xs):
                xss[tup[0]] += xs[tup[0]]
        return zip(es, xss)
    return None


def write_sum_of_xsecs(xsecs, flavor, current, target, min_e, max_e):
    """
    write the xsecs to file, with filename based on flavor, current, and
    target in the e-range defined by min_e and max_e
    """
    import re

    if xsecs is None:
        return

    fname = flavor + '_' + current + '_' + decode_target(target) + '.txt'
    fname = re.sub(r'\s+', '_', fname)
    xssum = 0.0
    seen_max_e = 0.0

    with open(fname, "w") as f:
        for tup in xsecs:
            en = float(tup[0])
            xs = float(tup[1]) / cm2 / 1e-38
            if en > min_e and en < max_e:
                xssum += xs
                seen_max_e = en
                print('{0:10.5f}:  {1:12.8f} x 10^(-38) cm2'.format(en, xs),
                      file=f)

        print("Erange " + str(min_e) + " to " + str(seen_max_e) + " sum = " +
              str(xssum) + " x 10^(-38) cm^2", file=f)


def spline_list_split(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage=__doc__)
    parser.add_option('-s', '--splines', type='string', action='callback',
                      callback=spline_list_split, dest='spline_files')
    parser.add_option('-t', '--target', type='string', default='1000060120',
                      help=r'Target PDG', dest='target')
    parser.add_option('-n', '--min', type='float', default=0.0,
                      help=r'Minimum energy', dest='min_e')
    parser.add_option('-x', '--max', type='float', default=120.0,
                      help=r'Maximum energy', dest='max_e')
    parser.add_option('--nc', default=True, action='store_false',
                      help=r'NC reactions', dest='is_cc')
    (options, args) = parser.parse_args()

    current = 'CC' if options.is_cc else 'NC'

    list_of_dicts = []
    for spline_file in options.spline_files:
        list_of_dicts.extend(xml_to_list_of_dicts(spline_file))

    muon_neutrinos = []
    muon_antineutrinos = []
    electron_neutrinos = []
    electron_antineutrinos = []

    for d in list_of_dicts:
        print(d['description'])
        if d['description']['tgt'] == options.target:
            if d['description']['flavor'] == 'Muon Neutrino' and \
                    decode_nc_cc(d['description']['proc']) == current:
                muon_neutrinos.append(d)
            if d['description']['flavor'] == 'Muon Antineutrino' and \
                    decode_nc_cc(d['description']['proc']) == current:
                muon_antineutrinos.append(d)
            if d['description']['flavor'] == 'Electron Neutrino' and \
                    decode_nc_cc(d['description']['proc']) == current:
                electron_neutrinos.append(d)
            if d['description']['flavor'] == 'Electron Antineutrino' and \
                    decode_nc_cc(d['description']['proc']) == current:
                electron_antineutrinos.append(d)

    flavors = ['Muon Neutrino', 'Muon Antineutrino',
               'Electron Neutrino', 'Electron Antineutrino']
    txsecs = [muon_neutrinos, muon_antineutrinos,
              electron_neutrinos, electron_antineutrinos]

    for x in zip(flavors, txsecs):
        total = sum_cross_section_dicts(x[1])
        write_sum_of_xsecs(total, x[0], current,
                           options.target,
                           options.min_e,
                           options.max_e)
