import warnings
from elasticsearch import Elasticsearch, RequestsHttpConnection
warnings.filterwarnings('ignore')

es = Elasticsearch('http://localhost:9200')

print (es.indices.analyze(index="french",body={
  "text" : "Je dois bosser pour mon QCM sinon je vais avoir une sale note :( ..."
}))
