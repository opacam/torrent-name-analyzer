#!/usr/bin/env python
# -*- coding: utf-8 -*-

from torrent_name_analyzer.name_parser.parse import PTN

ptn = PTN()


def parse(name):
    return ptn.parse(name)
