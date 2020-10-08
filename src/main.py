#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import logging as log

from util.Injector import Injector

import scrapper.main as scrapper_main

parser = argparse.ArgumentParser(description="Searcher-parser")
parser.add_argument("-cm", "--create_model", action='store_true', help="Create database in current directory")
parser.add_argument("-kw", "--keywords", type=str,
                    help="Keywords for searching", default='')
parser.add_argument("-c", "--count", type=int,
                    help="Sites count for parsing (default: 5)")
parser.add_argument("-ll", "--log_level", type=str,
                    default="INFO", help="Log level (default: INFO)")
parser.add_argument("-d", "--demo", action="store_true", help="Use demo mode. If demo = True create_model is True")
parser.add_help = True

args = parser.parse_args()

INJECTOR = Injector()

INJECTOR.get_db().connect()

log.basicConfig(filename="app.log",
                format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
                level=log._nameToLevel[args.log_level])

log.info("Passed arguments %s", args)

if __name__ == "__main__":
    log.info("Application started")

    if args.create_model or args.demo:
        import model
        log.info("Validation database schema")
        model.validate_database(INJECTOR.get_db())

    keywords: list = args.keywords.split(" ")
    count: int = args.count
    demo: bool = args.demo

    scrapper_main.main(keywords, count, demo)


INJECTOR.get_db().close()
