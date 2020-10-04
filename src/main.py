#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

from util.Injector import Injector

parser = argparse.ArgumentParser(description="Searcher-parser")
parser.add_argument("-cm", "--create_model", action='store_true')
parser.add_help = True

args = parser.parse_args()

INJECTOR = Injector()

INJECTOR.get_db().connect()

if __name__ == "__main__":
    if args.create_model:
        import model
        model.validate_database(INJECTOR.get_db())
    pass
    

INJECTOR.get_db().close()