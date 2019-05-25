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

DATE_HELP1 = 'DDMMAAAA'
DATE_HELP2 = 'DD/MM/AAAA'
DATE_HELP3 = 'DDMMAA'
DATE_HELP4 = 'DD/MM/AA'

DATE_FORMAT1 = '%d%m%Y'
DATE_FORMAT2 = '%d/%m/%Y'
DATE_FORMAT3 = '%d%m%y'
DATE_FORMAT4 = '%d/%m/%y'

DATE_FORMATS = [DATE_FORMAT1, DATE_FORMAT2, DATE_FORMAT3, DATE_FORMAT4]
DEFAULT_FORMAT = ['%Y-%m-%d']

def check_dir():
    '''Documentation for check_dir function'''

    # Create config directory if it doesn't exists
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # Initialize/Load JSON Data File
    ## Create if inexistent or empty
    if not os.path.exists(CONFIG_FILE) or os.stat(CONFIG_FILE).st_size == 0:
        with open(CONFIG_FILE, 'w') as data_file:
            date_list = []
            json.dump(date_list, data_file)
        print('Data file initialized!')

    ## Otherwise tries to load JSON file
    #TODO implement except handler in case of corrupted data
    else:
        with open(CONFIG_FILE, 'r') as data_file:
            date_list = json.load(data_file)
    return date_list

def add_date(date_str, date_list):
    '''Documentation for add_date function'''
    day = parse_date(date_str, DATE_FORMATS)
    day = str(day)
    date_list.append(day) if day not in date_list else date_list
    with open(CONFIG_FILE, 'w') as data_file:
        json.dump(date_list, data_file)
    return date_list

def remove_date(date_str, date_list):
    '''Documentation for remove_date function'''
    day = parse_date(date_str, DATE_FORMATS)
    day = str(day)
    if day in date_list: date_list.remove(day)
    with open(CONFIG_FILE, 'w') as data_file:
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
    if days_list:
       
        for day in days_list:
            day = parse_date(day, DEFAULT_FORMAT)
            date_diff = (day - today).days
            if date_diff!=1:
                print(f'Faltam {date_diff} dias para {day}')
            else:
                print(f'Falta {date_diff} dia para {day} (Amanhã)')
    else:
        print('There is no date registered.')
        print(' Use "days-left add DDMMYYYY" to store a date')

def flist(args):
    today = date.today()
    date_list = check_dir()
    print_list(today, date_list)

def fadd(args):
    date_str = args.date
    date_list = check_dir()
    add_date(date_str, date_list)
    # today = date.today()
    # print_list(today, date_list)

def fremove(args):
    date_str = args.date
    date_list = check_dir()
    remove_date(date_str, date_list)
    # today = date.today()
    # print_list(today, date_list)


def main():
    '''Main description'''

    # MainParser
    parser = argparse.ArgumentParser(
        description='Show days left of dates from today',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.set_defaults(func=flist)
    date_help = '''Date. Format accepted DDMMYYYY, DD/MM/YYYY
And others DD.MM.YYYY
DD-MM-YYYY
'''

    # SubParser
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_list = subparsers.add_parser('list', description='List days left', help='list days left (default)')
    parser_list.set_defaults(func=flist)

    parser_add = subparsers.add_parser('add', description='Add DATE', help='add date')
    parser_add.add_argument('date', metavar='DATE', type=str, help=date_help)
    parser_add.set_defaults(func=fadd)

    parser_rem = subparsers.add_parser('remove', description='Remove DATE', help='Remove date')
    parser_rem.add_argument('date', metavar='DATE', type=str, help=date_help)
    parser_rem.set_defaults(func=fremove)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())