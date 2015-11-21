#!/usr/bin/env python
# encoding: utf-8
import json
import traceback
import sys


def load_json(file_name):
    f = open(file_name, 'r')
    buff = f.read()
    f.close()
    return json.loads(buff)


def save_json(data, file_name):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def write_exc_info():
    '''Debug method, place it after an Exception is catched'''
    logfile = open('data/logfile.txt', 'w')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logfile.write("*** print_tb:")
    traceback.print_tb(exc_traceback, limit=1, file=logfile)
    logfile.write("*** print_exception:")
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=logfile)
    logfile.write("*** print_exc:")
    traceback.print_exc(file=logfile)
    logfile.write("*** format_exc, first and last line:")
    formatted_lines = traceback.format_exc().splitlines()
    logfile.write(formatted_lines[0])
    logfile.write(formatted_lines[-1])
    logfile.write("*** format_exception:")
    logfile.write(
        repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    logfile.write("*** extract_tb:")
    logfile.write(repr(traceback.extract_tb(exc_traceback)))
    logfile.write("*** format_tb:")
    logfile.write(repr(traceback.format_tb(exc_traceback)))
    logfile.write(
        str("*** tb_lineno:" + str(exc_traceback.tb_lineno)))
    logfile.close()
