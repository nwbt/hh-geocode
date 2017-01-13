#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.

from collections import OrderedDict
import csv
import sys
import os
import logging
import click
import re
import json

logfile = 'logs/csvToJson.txt'
loglevel = 'WARNING'
logmsg = '%(asctime)s|%(levelname)s|%(message)s'

class Store:

    def __init__(this, store_dict):
        this.store_dict = store_dict


class CSVFile:

    def __init__(this, filename):

        this.filename = filename
        this._create_store_list()

    def _create_store_list(this):
        
        this.store_list = []

        try:
            with open(this.filename) as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                try:
                    reader = csv.DictReader(csvfile, dialect=dialect)
                    for idx, row in enumerate(reader):
                        newrow = _rekey(row) 
                        this.store_list.append(newrow)

                except IOError as ioe:
                    logging.critical(ioe.strerror)

        except FileNotFoundError as fnfe:
            logging.critical(fnfe.strerror + ",filename:" + fnfe.filename)


def _rekey(row):

    exp = re.compile(r"""(^sl_)(.*$)""")
    rekeyed_row = OrderedDict()
    for key in row:
        match = exp.search(key)
        rekeyed_row[match.group(2)] = row[key]

    return rekeyed_row


class JSONFile:

    def __init__(this, filename):

        this.filename = filename


def open_and_read_file(filename):
    pass
    # todo log error and 

@click.command()
@click.argument('inputfile')
@click.option('--outputfile', '-o', default='resources/geolocations.json')
@click.option('--loglevel', '-l', default=loglevel)
@click.option('--logfile', '-f', default=logfile)
def csv_to_json(inputfile, outputfile, loglevel, logfile):

    logging.basicConfig(filename=logfile, level=loglevel.upper(), format=logmsg)
    csvfile = CSVFile(inputfile)
    pass

if __name__ == '__main__':
    
    csv_to_json()

