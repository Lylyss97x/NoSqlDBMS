import warnings
from elasticsearch import Elasticsearch, RequestsHttpConnection
warnings.filterwarnings('ignore')

es = Elasticsearch('http://localhost:9200')

#create
es.indices.create(index="first_index",ignore=400)

#verify
print (es.indices.exists(index="first_index"))

#delete
print (es.indices.delete(index="first_index", ignore=[400,404]))
