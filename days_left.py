#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from datetime import datetime, date, timedelta

import json
from json.decoder import JSONDecodeError

DATA_DIR_NAME = 'days-left'
DATA_FILE_NAME = 'dates.json'

CONFIG_DIR = os.getenv('HOME')
CONFIG_DIR = os.path.join(CONFIG_DIR, '.config', DATA_DIR_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, DATA_FILE_NAME)

print('CONFIG_DIR:', CONFIG_DIR)

DATE_HELP1 = 'DDMMAAAA'
DATE_HELP2 = 'DD/MM/AAAA'
DATE_HELP3 = 'DDMMAA'
DATE_HELP4 = 'DD/MM/AA'

DATE_FORMAT1 = '%d%m%Y'
DATE_FORMAT2 = '%d/%m/%Y'
DATE_FORMAT3 = '%d%m%y'
DATE_FORMAT4 = '%d/%m/%y'

DATE_FORMATS = [DATE_FORMAT1, DATE_FORMAT2, DATE_FORMAT3, DATE_FORMAT4]

def check_dir():
    '''Documentation for check_dir function'''
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w+') as data_file:
        try:
            date_list = json.load(data_file)
        except JSONDecodeError as err:
            date_list = []
            json.dump(date_list, data_file)
    return date_list

def parse_date(date_str, date_formats_list):
    '''Documentation for parse_date function'''
    for date_format in date_formats_list:
        try:
            date_var = datetime.strptime(date_str, date_format)
            return date_var.date()
        except ValueError:
            pass

def print_list(today, days_list):
    '''Documentation for print_list function'''
    for day in days_list:
        day = parse_date(day, DATE_FORMATS)
        date_diff = (day - today).days
        if date_diff!=1:
            print(f'Faltam {date_diff} dias para {day}')
        else:
            print(f'Falta {date_diff} dia para {day} (Amanhã)')

def main():
    '''Main description'''
    parser = argparse.ArgumentParser(
        description='Program description',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    #add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
    parser.add_argument('a', type=int, nargs='*', default=1, help='A int var a')
    args = parser.parse_args()
    print('Hello Underworld!\nargs: %s' % (args))

    # Check dir and create file

    today = date.today()
    days_list = [
        '21/10/2018',
        '22/10/2018',
        '23/10/2018',
        '05/11/2018',
        '12/11/2018',
        '14/11/2018',
        '26/11/2018',
        '10/12/2018',
        '6/07/2019',
        '25/05/2019',
    ]
    print_list(today, days_list)

    # while(True):
    #     print('Insira a data')
    #     print('({}, {}, {} ou {}): '.format(DATE_HELP1, DATE_HELP2, DATE_HELP3, DATE_HELP4), end = '')
    #     date_input = input()
    #     date_output = parse_date(date_input, DATE_FORMATS)
    #     if date_output:
    #         print('Confirmação: {}'.format(date_output))
    #     else:
    #         print('Erro ao ler {}'.format(date_input))



if __name__ == '__main__':
    sys.exit(main())