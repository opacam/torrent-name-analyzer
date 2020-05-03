#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import unittest

from torrent_name_analyzer.name_parser import ptn

CURRENT_DIR = os.path.dirname(__file__)


class ParseTest(unittest.TestCase):
    def test_parser(self):
        json_input = os.path.join(CURRENT_DIR, "files/input.json")
        with open(json_input) as input_file:
            torrents = json.load(input_file)

        json_output = os.path.join(CURRENT_DIR, "files/output.json")
        with open(json_output) as output_file:
            expected_results = json.load(output_file)

        self.assertEqual(len(torrents), len(expected_results))

        test_number = 0
        for torrent, expected_result in zip(torrents, expected_results):
            test_number += 1
            print(f"Test {test_number}: {torrent}")
            result = ptn.parse(torrent)
            for key in expected_result:
                self.assertIn(key, result)
                self.assertEqual(result[key], expected_result[key])


if __name__ == "__main__":
    unittest.main()
