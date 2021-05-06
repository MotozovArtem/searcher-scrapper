#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import logging as log

from util.Injector import Injector

from scrapper.main import main as scrapper_main


# Обычно выделяют в отдельный метод
def myParser():
    parser = argparse.ArgumentParser(description="Searcher-parser")
    parser.add_argument(
        "-cm", 
        "--create_model", 
        action='store_true', 
        dest="create_model_", 
        required = False, 
        help="Create database in current directory"
        )
    parser.add_argument(
        "-kw", 
        "--keywords", 
        type=str, 
        dest="keywords_", 
        required = False, 
        help="Keywords for searching", 
        default=''
        )
    parser.add_argument(
        "-sc", 
        "--site-count", 
        type=int, 
        dest="site_count_", 
        required = False, 
        help="Sites count for parsing (default: 5)", 
        default=5
        )
    parser.add_argument(
        "-ll", 
        "--log_level", 
        type=str, 
        dest="log_level_", 
        required = False, 
        help="Log level (default: INFO)", 
        default="INFO"
        )
    parser.add_argument(
        "-dm", 
        "--demo-mode", 
        action="store_true", 
        dest="demo_mode_", 
        required = False, 
        help="Use demo mode. If demo = True create_model is True")
    parser.add_help = True

    return parser.parse_args()


def main(create_model, keywords, site_count, log_level, demo_mode):
    INJECTOR = Injector()
    INJECTOR.get_db().connect()

    log.basicConfig(filename="app.log",
                format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
                level=log._nameToLevel[log_level])

    log.info("Application started")

    if create_model or demo_mode:
        import model
        log.info("Validation database schema")
        model.validate_database(INJECTOR.get_db())

    keywords = keywords.split(" ")

    scrapper_main(keywords, site_count, demo_mode)

    INJECTOR.get_db().close()


if __name__ == "__main__":
    # Сюда по возможности пишут как можно меньше логики
    input_args = myParser()
    # Вроде будет не очень красивый вывод, но для красивого нужно будет немного порвать ASS
    log.info("Passed arguments %s", input_args)
    main(
        input_args.create_model_, 
        input_args.keywords_, 
        input_args.site_count_, 
        input_args.log_level_, 
        input_args.demo_mode_
        )
