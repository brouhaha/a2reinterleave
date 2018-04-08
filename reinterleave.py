#!/usr/bin/env python3

# Copyright 2018 Eric Smith <spacewar@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of version 3 of the GNU General Public License
# as published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse


def list_to_dict(l):
    return { i: l[i] for i in range(len(l)) }

def invert_dict(d):
    return { v: k for k, v in d.items() }

def compose_dict(d1, d2):
    return { k: d2[v] for k, v in d1.items() }


def reinterleave(src_image, src_interleave, dest_interleave):
    map = compose_dict(src_interleave, invert_dict(dest_interleave))
    dest_image = bytearray(len(src_image))
    for t in range(35):
        for ss in range(16):
            src_offset = (t * 16 + ss) * 256
            dest_offset = (t * 16 + map[ss]) * 256
            dest_image[dest_offset:dest_offset+256] = src_image[src_offset:src_offset+256]
    return dest_image


half_block_to_phys_sect = list_to_dict([0x00, 0x02, 0x04, 0x06,
                                        0x08, 0x0a, 0x0c, 0x0e,
                                        0x01, 0x03, 0x05, 0x07,
                                        0x09, 0x0b, 0x0d, 0x0f])

dos_to_phys_sect = list_to_dict([0x0, 0xd, 0xb, 0x9, 0x7, 0x5, 0x3, 0x1,
                                 0xe, 0xc, 0xa, 0x8, 0x6, 0x4, 0x2, 0xf])

identity = { k: k for k in range(16) }



interleave_tables = { 'dos':    dos_to_phys_sect,
                      'do':     dos_to_phys_sect,
                      'pascal': half_block_to_phys_sect,
                      'phys':   identity,
                      'po':     half_block_to_phys_sect,
                      'prodos': half_block_to_phys_sect,
                      'sos':    half_block_to_phys_sect }


parser = argparse.ArgumentParser()

parser.add_argument('infmt',
                    type = str,
                    choices = sorted(interleave_tables.keys()))

parser.add_argument('infile',
                    type = argparse.FileType('rb'))

parser.add_argument('outfmt',
                    type = str,
                    choices = sorted(interleave_tables.keys()))

parser.add_argument('outfile',
                    type = argparse.FileType('wb'))

args = parser.parse_args()

input_image = args.infile.read()

output_image = reinterleave(input_image, interleave_tables[args.infmt], interleave_tables[args.outfmt])

args.outfile.write(output_image)

