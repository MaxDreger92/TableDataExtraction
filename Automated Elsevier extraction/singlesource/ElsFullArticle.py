#! /usr/bin/env python
"""
This file contains the ElsevierFullArticle class.
The ElsevierFullArticle class has a read(), write() function. The read()
function needs a ElsevierClient object as argument and adds the data of a full
article to its data member.
The write() member function is using the data mamber, created by read() and
writes it into a file, the path of the file is defined wire the a ElsevierClient
object.
"""

import requests
import json
from pathlib import Path





class ElsevierFullArticle():

    base_url = u'https://api.elsevier.com/content/article/'

    def __init__(self, uri ='', pii='', doi=''):
        if uri and not pii and not doi:
            self._uri = uri;
        elif pii and not uri and not doi:
            self._uri = self.base_url+ 'pii/' +str(pii)
        elif doi and not uri and not pii:
            self._uri = self.base_url + 'doi/' + str(doi)
        elif not uri and not pii and not doi:
            raise ValueError ('Need doi, pii or URI')
        elif (doi and pii) or (doi and uri) or (pii and uri):
            raise ValueError ('Too much input')

    def read(self, ElsevierClient, format):
        if format == ('pdf' or 'PDF' or 'Pdf'):
            ElsevierClient.format = 'application/pdf'
        elif format == 'xml' or 'XML' or 'Xml':
            # print("test")
            ElsevierClient.format = 'text/xml'
        print("0")
        self.data, self.bool = ElsevierClient.make_request(self._uri)
        print("1")
        if self.bool == True:
            print("2")
            ## TODO: better format handling ###
            try:
                print("3")
                # print(self.data.headers['Content-Type'][12:])
                self.format = self.data.headers['Content-Type'][12:]
            except:
                self.format = ''
            return True
        else:
            print("4")
            return False



    def write(self, ElsevierClient, path):

        if self.data:
            filename = Path(path)
            filename.write_bytes(self.data.content)
            print(str(ElsevierClient.saving_path) + '/' +path)
            print(ElsevierClient.saving_path)
            print("Data has been written to: "+ path)
            return True
        else:
            print("No Data available")
            return False








    def retrieve_pdf(self, path, ElsevierClient, name):
        if ElsevierClient:
            self._ElsevierClient = ElsevierClient;
        elif not self.ElsevierClient:
            raise("You have no Power here! Create Client or give one as an arguement")
        response = requests.get(self._uri, headers = ElsevierClient.headers)
        filename = Path(ElsevierClient.path+name)
        filename.write_bytes(response.content)
