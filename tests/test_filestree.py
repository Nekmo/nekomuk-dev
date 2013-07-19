#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import unittest
import os
if __name__ == '__main__':
    import sys
    sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))
from nekomuk import filestree

DIRNAME = os.path.dirname(os.path.abspath(__file__))

class TestFilesTree(unittest.TestCase):
    def setUp(self):
        path = os.path.join(DIRNAME, 'testdir')
        self.tree = filestree.Tree(path)
        
    def test_files_in_subdir(self):
        print(self.tree)
        self.assertEqual(len(self.tree.dirs[1].files), 2)
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()