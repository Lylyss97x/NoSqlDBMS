import warnings
from elasticsearch import Elasticsearch, RequestsHttpConnection
warnings.filterwarnings('ignore')

es = Elasticsearch('http://localhost:9200')


res = es.search(index="cities", body={"query":{"match_all":{}}})
print (res)
