#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/11/19 15:58
# @File     : test_decode_venn_data
# @Project  : Toolbox
# @Desc     :

import unittest

from src.venn.decode_venn_data import decode_venn_data


class TestDecodeVennData(unittest.TestCase):

    def decode_venn_data_single_set(self):
        data = {'a': {1, 2, 3}}
        expected = {('a',): {1, 2, 3}}
        result = decode_venn_data(data)
        self.assertEqual(result, expected)

    def decode_venn_data_disjoint_sets(self):
        data = {'a': {1, 2, 3}, 'b': {4, 5, 6}}
        expected = {('a',): {1, 2, 3}, ('b',): {4, 5, 6}}
        result = decode_venn_data(data)
        self.assertEqual(result, expected)

    def decode_venn_data_overlapping_sets(self):
        data = {'a': {1, 2, 3}, 'b': {2, 3, 4}}
        expected = {('a',): {1}, ('b',): {4}, ('a', 'b'): {2, 3}}
        result = decode_venn_data(data)
        self.assertEqual(result, expected)

    def decode_venn_data_empty_sets(self):
        data = {'a': set(), 'b': set()}
        expected = {('a',): set(), ('b',): set()}
        result = decode_venn_data(data)
        self.assertEqual(result, expected)

    def decode_venn_data_no_intersection(self):
        data = {'a': {1, 2}, 'b': {3, 4}, 'c': {5, 6}}
        expected = {('a',): {1, 2}, ('b',): {3, 4}, ('c',): {5, 6}}
        result = decode_venn_data(data)
        self.assertEqual(result, expected)

    def decode_venn_data_full_intersection(self):
        data = {'a': {1, 2}, 'b': {1, 2}, 'c': {1, 2}}
        expected = {('a', 'b', 'c'): {1, 2}}
        result = decode_venn_data(data)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()