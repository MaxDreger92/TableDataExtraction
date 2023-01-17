import pandas as pd, json, requests
from urllib.parse import quote as url_encode
# from els_client import Elsevier_client
import pprint
from singlesource.ElsFullArticle import ElsevierFullArticle
class SciencedirectSearch():

    search_base_url = u'https://api.elsevier.com/content/search/sciencedirect'
    metadata_base_url = u'https://api.elsevier.com/content/metadata/article'

    def __init__(self, query, Elsevier_client):
        """Initializes a search object with a query and target index."""
        print(query.query)
        self.query = "title(" + " OR ".join(query.query["title"]) + ") AND keywords(" + \
        " OR ".join(query.query["keywords"]) + ") AND abstract(" + " OR ".join(query.query["abstract"]) +")"
        print("init",self.query)
        self._sd_metadata_url = self.metadata_base_url + '?query=' + url_encode(self.query)
        self._sd_search_url = self.search_base_url +'?count=' + str(query.query["count"] )+ '&start=' + \
        str(query.query['start']) + '&year=' + str(query.query['year'][0]) + '-' \
        + str(query.query['year'][1]) + '&query=' + url_encode(self.query) 
        self._sd_author_doi={}

        # self._sd_uri = "https://api.elsevier.com/content/search/sciencedirect?query=KEY%28ink%20OR%20catalyst%20ink%20OR%20KEY%28nafion%20OR%20NAFION%29%29


    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query


    def search_sciencedirect (self, Elsevier_client = None):
        print("query:", self._sd_search_url)
        self._sd_results = Elsevier_client.make_request(self._sd_search_url)
        self._results =self._sd_results[0].json()
        print(json.dumps(self._results, indent= 2), file=open("results", "a"))
        

    def get_articles_from_sdsearch (self, ElsevierClient=None):
        for result in self._results['search-results']['entry']:
            e_art = ElsevierFullArticle(pii = result['pii']) 
            e_art.read(ElsevierClient, "pdf")
            e_art.write(ElsevierClient, result['pii'] + ".pdf")
            
    def search_meta_data_elsevier (self, Elsevier_client = None):
        self._sd_results = Elsevier_client.make_request(self._sd_metadata_url)
        # print("JSON", self._sd_results.json())
        print(self._sd_results.json()["search-results"]["opensearch:totalResults"])
        for i in self._sd_results.json()["search-results"]["entry"]:
            self._sd_author_doi[i["dc:title"]] = i["dc:identifier"]
        print(self._sd_author_doi)
