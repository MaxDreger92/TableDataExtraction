#! /usr/bin/env python
"""
This file contains the main() function. It imports all necessary classes and
starts a search, retrieves PDFs and adds them to an SQL data base
"""
from singlesource.ElsClient import ElsevierClient
from singlesource.ElsSearch import SciencedirectSearch
from query.GetQuery import CreateQuery
import json
import requests
from pathlib import Path

query = CreateQuery("Keywords")
e_client = ElsevierClient('f805979fee59e4f619d85fa9f8e661c3', saving_path = None)
SciencedirectSearch = SciencedirectSearch(query, e_client)
SciencedirectSearch.search_sciencedirect(e_client)
