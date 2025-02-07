Ingestion de Données avec Elasticsearch et Logstash
Ce projet montre comment ingérer des données dans Elasticsearch à l'aide de Logstash. Nous utiliserons Docker pour mettre en place l'ELK Stack (Elasticsearch, Logstash, Kibana) et effectuer l'ingestion de données depuis des fichiers CSV et JSON.

Prérequis
Docker et Docker Compose doivent être installés sur ta machine.
Architecture
L'architecture de ce projet ressemble à ceci :

kotlin
Copier
├── data
│   ├── data.csv
│   └── data-json.log
├── docker-compose.yml
├── elasticsearch
│   └── elasticsearch.yml
└── logstash
    ├── logstash.conf
    └── logstash.yml
Étapes
1. Créer le répertoire du projet
bash
Copier
mkdir elk-csv && cd elk-csv
2. Fichier docker-compose.yml
Crée un fichier docker-compose.yml pour configurer Elasticsearch, Logstash et Kibana dans des conteneurs Docker. Ce fichier permet de démarrer l'ELK Stack avec une seule commande.

yaml
Copier
version: "3"
services:
  elasticsearch:
    image: elasticsearch:7.6.2
    container_name: elasticsearch
    hostname: elasticsearch
    restart: always
    environment:
      - "discovery.type=single-node"
    ports:
      - 9200:9200
      - 9300:9300
    networks:
      - dockerelk
    volumes:
      - ./elasticsearch/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml

  logstash:
    image: logstash:7.6.2
    container_name: logstash
    hostname: logstash
    ports:
      - 9600:9600
      - 8089:8089
    restart: always
    links:
      - elasticsearch:elasticsearch
    depends_on:
      - elasticsearch
    networks:
      - dockerelk
    volumes:
      - ./logstash/logstash.yml:/usr/share/logstash/config/logstash.yml
      - ./logstash/logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: kibana:7.6.2
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    networks:
      - dockerelk
    depends_on:
      - elasticsearch

networks:
  dockerelk:
    driver: bridge
3. Configurer Elasticsearch
Crée un répertoire elasticsearch et ajoute le fichier de configuration elasticsearch.yml pour définir les paramètres de ton nœud Elasticsearch :

yaml
Copier
cluster.name: docker-cluster
node.name: docker-node
node.master: true
network.host: 0.0.0.0
4. Configurer Logstash
Crée un répertoire logstash et ajoute le fichier de configuration logstash.conf pour définir comment Logstash ingère les données CSV ou JSON et les envoie à Elasticsearch.

Pour les données CSV :
bash
Copier
mkdir logstash && cd logstash
touch logstash.conf
Le contenu de logstash.conf pour un fichier CSV :

plaintext
Copier
input {
  file {
    path => "/usr/share/logstash/external-data/data.csv"
    start_position => "beginning"
    sincedb_path => "/dev/null"
  }
}

filter {
  csv {
    separator => ","
    columns => ["order_id", "order_date", "customer_name", "product_name", "quantity", "price"]
  }

  date {
    match => ["order_date", "yyyy-MM-dd"]
    target => "order_date"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "orders-%{+YYYY.MM.dd}"
  }
}
Pour les données JSON :
Le contenu de logstash-json.conf pour un fichier JSON :

plaintext
Copier
input {
  file {
    start_position => "beginning"
    path => "/usr/share/logstash/external-data/data-json.log"
    sincedb_path => "/dev/null"
  }
}

filter {
  json {
    source => "message"
  }
  mutate {
    remove_field => ["message","host","@timestamp","path","@version"]
  }
}

output {
   elasticsearch {
    hosts => "elasticsearch:9200"
    index => "your-index-name"
   }
   stdout{}
}

5. Démarrer l'ELK Stack avec Docker Compose
Dans le répertoire racine de ton projet, utilise Docker Compose pour démarrer les services :

bash
Copier
docker-compose up
Cette commande démarre Elasticsearch, Logstash et Kibana dans des conteneurs Docker.

6. Tester la configuration de Logstash
Avant de démarrer Logstash, tu peux tester la configuration de Logstash pour vérifier qu'il n'y a pas d'erreurs dans ton fichier logstash.conf :

bash
Copier
docker-compose exec logstash bin/logstash --config.test_and_exit -f /usr/share/logstash/pipeline/logstash.conf
Si tout est correct, tu devrais voir la sortie suivante :

plaintext
Copier
Configuration OK
7. Accéder à Kibana
Une fois l'ELK Stack en marche, tu peux accéder à Kibana en ouvrant ton navigateur à l'adresse suivante :

arduino
Copier
http://localhost:5601
Cela te permettra de visualiser et analyser tes données ingérées dans Elasticsearch via l'interface graphique de Kibana.

8. Vérification des données dans Elasticsearch
Après que Logstash ait ingéré les données, tu peux vérifier que les données ont bien été indexées dans Elasticsearch en utilisant cURL :

bash
Copier
curl -X GET "localhost:9200/csv-data/_search?q=*" | jq
