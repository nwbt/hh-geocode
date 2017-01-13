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

class Store:

    def __init__(this, row):

        if type(row) is not OrderedDict or len(row) != 20:
            # log error and return
            return
       
        try:
            this.id = row['sl_id']
            this.store = row['sl_store']
            this.address = row['sl_address']
            this.address2 = row['sl_address2']
            this.city = row['sl_city']
            this.state = row['sl_state']
            this.zip = row['sl_zip']
            this.country = row['sl_country']
            this.latitude = row['sl_latitude']
            this.longitude = row['sl_longitude']
            this.tags = row['sl_tags']
            this.description = row['sl_description']
            this.email = row['sl_email']
            this.url = row['sl_url']
            this.hours = row['sl_hours']
            this.phone = row['sl_phone']
            this.fax = row['sl_fax']
            this.image = row['sl_image']
            this.private = row['sl_private']
            this.neat_title = row['sl_neat_title']

        except AttributeError as e:
            
            # log as error 
            print("\n\n" + str(e) + " : " + str(row) + "\n\n")
            return


class CSVFile:

    def __init__(this, filename):

        this.filename = filename

    def get_store_list(this):
        
        this.store_list = []

        with open(this.filename) as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            try:
                reader = csv.DictReader(csvfile, dialect=dialect)
                for idx, row in enumerate(reader):
                    newrow = _rekey(row) 
                    this.store_list.append(newrow)

            except IOError as ie:
                # todo log and print
                pass

        

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
def csv_to_json(inputfile, outputfile):

    csvfile = CSVFile(inputfile)
    store_dict = csvfile.get_store_list()
    pass

if __name__ == '__main__':
    
    csv_to_json()

#    store_list = []
#
#        for idx, row in enumerate(reader):
#
#            try:
#                store = Store(row)
#                store_list.append(store)
#            
#            except AttributeError as ae:
#                // todo log errors
#                print("error parsing csvfile, line: " + idx 
#                        + ", error:" + str(ae))
#
