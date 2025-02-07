import warnings
from elasticsearch import Elasticsearch, RequestsHttpConnection
warnings.filterwarnings('ignore')

es = Elasticsearch('http://localhost:9200')

#afficher les cities qui commencent par L
print (es.search(index="cities", body={"query": {"regexp" : { "city" : "l.*" }}}))
