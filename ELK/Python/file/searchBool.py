import warnings
from elasticsearch import Elasticsearch, RequestsHttpConnection
warnings.filterwarnings('ignore')

es = Elasticsearch('http://localhost:9200')

print (es.search(index="movies", body=
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "fields.directors": "George"
          }
        },
        {
          "match": {
            "fields.title": "Star Wars"
          }
        }
      ]
    }
  }
}))
