#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

from util.Injector import Injector

import scrapper.main as scrapper_main

parser = argparse.ArgumentParser(description="Searcher-parser")
parser.add_argument("-cm", "--create_model", action='store_true')
parser.add_argument("-g", "--gui", action="store_true", help="Graphic mode")
parser.add_argument("-kw", "--keywords", type=tuple, help="Keywords for searching")
parser.add_argument("-c", "--count", type=int, help="Sites count for parsing (default: 5)")
parser.add_help = True

args = parser.parse_args()

INJECTOR = Injector()

INJECTOR.get_db().connect()

if __name__ == "__main__":
    if args.create_model:
        import model
        model.validate_database(INJECTOR.get_db())
    
    scrapper_main.main()
    

INJECTOR.get_db().close()