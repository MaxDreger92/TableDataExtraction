#! /usr/bin/env python
"""
This file contains the CreateQuery class. The constructor takes a file as its
argument and adds its content as a dictionary to its query data member
"""

import ast


class CreateQuery ():
    def __init__(self, file):
        with open(file, "r") as data:
            self.query = ast.literal_eval(data.read())
