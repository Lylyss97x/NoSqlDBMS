import warnings
from elasticsearch import Elasticsearch, RequestsHttpConnection
warnings.filterwarnings('ignore')

es = Elasticsearch('http://localhost:9200')

doc1 = {"text" : "Une phrase en français :) ..."}
print (es.index(index="french", id=1, body=doc1))
