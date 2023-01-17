#! /usr/bin/env python
"""
This file contains the ElsevierClient class.
The ElsevierClient class has a make_request() member function.
The make_request() takes an URL as an input and returns a response object.
The ElsevierClient object has and apiKey as a data member, as well as a
saving_path sata member.
"""

import pathlib
import requests
import json




class ElsevierClient:

    __url_base = "https://api.elsevier.com/"

    def __init__(self, apiKey, saving_path=None):
        self.apiKey = apiKey
        self.format = 'application/json'

        if not saving_path:
            self.saving_path = pathlib.Path.cwd() / 'data'
        else:
            self.saving_path = pathlib.Path(saving_path)

    @property
    def apiKey(self):
        return self._apiKey

    @apiKey.setter
    def apiKey (self, apiKey):
        self._apiKey = apiKey

    @property
    def saving_path(self):
        return self._saving_path

    @saving_path.setter
    def saving_path(self, saving_path):
        self._saving_path = saving_path

    @property
    def format(self):
        return self._format

    @format.setter
    def format (self, format):
        self._format = format


    def make_request(self, URL):
        self.headers = {
                    "X-ELS-APIKey"  : self.apiKey,
                    "Accept"        : self.format
                    }
        ## TODO: implementn throttle ##

        # print(self.headers)
        r = requests.get(URL, headers = self.headers)
        print(r.headers, file=open("headers_els.txt", "a"))
        self._status = r.status_code
        print(r.headers)
        if self._status == 200:
            print("It worked out fine")
            return r, True
        else:
            print("\nThere is something wrong with your request, please check the header for more information!\n")
            return "No data", False
