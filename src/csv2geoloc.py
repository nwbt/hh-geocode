#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.

from collections import OrderedDict
from googlemaps import geocoding
from googlemaps import client
import argparse
import csv
import sys
import os
import logging
import re
import json

logfile = 'logs/csvToJson.txt'
loglevel = 'WARNING'
logmsg = '%(asctime)s|%(levelname)s|%(message)s'
gkey = ''


class Store:

    def __init__(this, store_dict):
        this.id = store_dict['id']
        this.store = store_dict['store']
        this.address = store_dict['address']
        this.address2 = store_dict['address2']
        this.city = store_dict['city']
        this.state = store_dict['state']
        this.zip = store_dict['zip']
        this.country = store_dict['country']
        this.latitude = store_dict['latitude']
        this.longitude = store_dict['longitude']
        this.tags = store_dict['tags']
        this.email = store_dict['email']
        this.url = store_dict['url']
        this.hours = store_dict['hours']
        this.phone = store_dict['phone']
        this.fax = store_dict['fax']
        this.image = store_dict['image']
        this.private = store_dict['private']
        this.neat_title = store_dict['neat_title']
        this.description = store_dict['description']

    def full_address(this):
        return this.store 

def build_store_list_from_csv(filename):
    
    store_list = []

    try:
        with open(filename) as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            try:
                reader = csv.DictReader(csvfile, dialect=dialect)
                for idx, row in enumerate(reader):
                    newrow = _rekey(row) 
                    store_list.append(Store(newrow))

            except IOError as ioe:
                logging.critical(ioe.strerror)
                return

    except FileNotFoundError as fnfe:
        logging.critical(fnfe.strerror + ",filename:" + fnfe.filename)
        return

    return store_list

def _rekey(row):
    exp = re.compile(r"""(^sl_)(.*$)""")
    rekeyed_row = {} 
    for key in row:
        match = exp.search(key)
        rekeyed_row[match.group(2)] = row[key]

    return rekeyed_row

def start():
    cli = CommandLineInput()
    logging.basicConfig(filename=cli.args.logfile, level=cli.args.loglevel.upper(), format=logmsg)
    store_list = build_store_list_from_csv(cli.args.inputfile)
    pass


class CommandLineInput():

    def __init__(this):
        parser = argparse.ArgumentParser()
        this.args = _build_argument_list(parser)

    def _inputfile(this):
        # todo verify file exists
        pass

    def _apikey(this):
        # todo verify exists works
        pass

    def _outputfile(this):
        # verify path exists & okay to overwrite
        pass

    def _loglevel(this):
        # verify logging level is valid
        pass

    def _logfile(this):
        # verify path exists and appendable
        pass 


def _build_argument_list(parser):
    parser.add_argument('inputfile', help='', type=str)
    parser.add_argument('--apikey', '-k', help='', type=str, default='resources/secrets')
    parser.add_argument('--outputfile', '-o', help='', type=str, default='resources/geolocations.json')
    parser.add_argument('--loglevel', '-l', help='', type=str, default='WARNING')
    parser.add_argument('--logfile', '-f', help='', type=str, default='logs/logfile.txt')
    return parser.parse_args()


if __name__ == '__main__':
    start()

