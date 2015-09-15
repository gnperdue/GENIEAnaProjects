#!/usr/bin/env python
"""
Flux convolution
"""
from __future__ import print_function


def findxs(en, xsecs):
    low_idx = 0
    high_idx = len(xsecs) - 1
    mid_idx = int((high_idx + low_idx) / 2)
    energy = xsecs[mid_idx][0]
    while high_idx - low_idx > 1:
        if en > energy:
            low_idx = mid_idx
            mid_idx = int((high_idx + low_idx) / 2)
            energy = xsecs[mid_idx][0]
        elif en < energy:
            high_idx = mid_idx
            mid_idx = int((high_idx + low_idx) / 2)
            energy = xsecs[mid_idx][0]
        else:
            break

    return xsecs[mid_idx][1]


def fconvolve(flux_file, xsec_file, emin, emax):
    import re

    xsec = []
    with open(xsec_file, "r") as xs:
        for line in xs.readlines():
            if re.search(':', line):
                line = line.rstrip()
                bits = line.split(':')
                en = float(bits[0].strip())
                xs = float(bits[1].split('x')[0].strip())
                xsec.append((en, xs))

    bin_lows = []
    counts = []
    sum = 0.0
    with open(flux_file, "r") as fx:
        for line in fx.readlines():
            if re.search('TH1', line):
                continue
            bits = line.split(',')
            bits = [s.strip() for s in bits]
            count = float(bits[0].split('=')[1])
            bin_low = float(bits[1].split('=')[1])
            if bin_low < emin or bin_low > emax:
                continue
            bin_lows.append(bin_low)
            counts.append(count)
            sum += count

    counts = [v / sum for v in counts]
    bins = zip(bin_lows[0:-1], bin_lows[1:])
    flux = zip(bins, counts)  # drop overflow bin

    total_xsec = 0.0
    for tup in flux:
        bin_center = (tup[0][1] + tup[0][0]) / 2.0
        weight = tup[1]
        weightedxs = findxs(bin_center, xsec) * weight
        total_xsec += weightedxs

    return total_xsec


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage=__doc__)
    parser.add_option('-n', '--min', type='float', default=0.0,
                      help=r'Minimum energy', dest='min_e')
    parser.add_option('-x', '--max', type='float', default=120.0,
                      help=r'Maximum energy', dest='max_e')
    (options, args) = parser.parse_args()

    labels = ['Anti-electron neutrino', 'Electron neutrino',
              'Anti-muon neutrino', 'Muon neutrino']

    flux_files = ['electron_antinu_flux.txt', 'electron_nu_flux.txt',
                  'muon_antinu_flux.txt', 'muon_nu_flux.txt']

    carbon_cc_files = ['Electron_Antineutrino_CC_Carbon.txt',
                       'Electron_Neutrino_CC_Carbon.txt',
                       'Muon_Antineutrino_CC_Carbon.txt',
                       'Muon_Neutrino_CC_Carbon.txt']

    carbon_nc_files = ['Electron_Antineutrino_NC_Carbon.txt',
                       'Electron_Neutrino_NC_Carbon.txt',
                       'Muon_Antineutrino_NC_Carbon.txt',
                       'Muon_Neutrino_NC_Carbon.txt']

    hydrogen_cc_files = ['Electron_Antineutrino_CC_Hydrogen.txt',
                         'Electron_Neutrino_CC_Hydrogen.txt',
                         'Muon_Antineutrino_CC_Hydrogen.txt',
                         'Muon_Neutrino_CC_Hydrogen.txt']

    hydrogen_nc_files = ['Electron_Antineutrino_NC_Hydrogen.txt',
                         'Electron_Neutrino_NC_Hydrogen.txt',
                         'Muon_Antineutrino_NC_Hydrogen.txt',
                         'Muon_Neutrino_NC_Hydrogen.txt']

    rein_cc_files = ['ReinDFRPXSec_Electron_Antineutrino_CC_on_Hydrogen.txt',
                     'ReinDFRPXSec_Electron_Neutrino_CC_on_Hydrogen.txt',
                     'ReinDFRPXSec_Muon_Antineutrino_CC_on_Hydrogen.txt',
                     'ReinDFRPXSec_Muon_Neutrino_CC_on_Hydrogen.txt']

    rein_nc_files = ['ReinDFRPXSec_Electron_Antineutrino_NC_on_Hydrogen.txt',
                     'ReinDFRPXSec_Electron_Neutrino_NC_on_Hydrogen.txt',
                     'ReinDFRPXSec_Muon_Antineutrino_NC_on_Hydrogen.txt',
                     'ReinDFRPXSec_Muon_Neutrino_NC_on_Hydrogen.txt']

    print('CC Carbon')
    for i in range(4):
        xs = fconvolve(flux_files[i], carbon_cc_files[i],
                       options.min_e, options.max_e)
        print(labels[i] + ' CC on Carbon total xsec = ' +
              str(xs) + ' x 10^(-38) cm2')

    print()

    print('NC Carbon')
    for i in range(4):
        xs = fconvolve(flux_files[i], carbon_nc_files[i],
                       options.min_e, options.max_e)
        print(labels[i] + ' NC on Carbon total xsec = ' +
              str(xs) + ' x 10^(-38) cm2')

    print()

    print('CC Hydrogen')
    for i in range(4):
        xs = fconvolve(flux_files[i], hydrogen_cc_files[i],
                       options.min_e, options.max_e)
        print(labels[i] + ' CC on Hydrogen total xsec = ' +
              str(xs) + ' x 10^(-38) cm2')

    print()

    print('NC Hydrogen')
    for i in range(4):
        xs = fconvolve(flux_files[i], hydrogen_nc_files[i],
                       options.min_e, options.max_e)
        print(labels[i] + ' NC on Hydrogen total xsec = ' +
              str(xs) + ' x 10^(-38) cm2')

    print()

    print('Rein CC Hydrogen')
    for i in range(4):
        xs = fconvolve(flux_files[i], rein_cc_files[i],
                       options.min_e, options.max_e)
        print(labels[i] + ' CC on Hydrogen total xsec = ' +
              str(xs) + ' x 10^(-38) cm2')

    print()

    print('Rein NC Hydrogen')
    for i in range(4):
        xs = fconvolve(flux_files[i], rein_nc_files[i],
                       options.min_e, options.max_e)
        print(labels[i] + ' NC on Hydrogen total xsec = ' +
              str(xs) + ' x 10^(-38) cm2')
