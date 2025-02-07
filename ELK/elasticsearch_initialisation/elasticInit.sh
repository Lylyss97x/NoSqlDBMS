#!/bin/bash

# Vérifier l'état du cluster
echo "Vérification de l'état du cluster..."
curl -s 0.0.0.0:9200/_cluster/health | jq

# Attendre un peu avant la commande suivante
sleep 2

# Vérifier les nœuds du cluster
echo "Vérification des nœuds du cluster..."
curl -s -X GET "http://0.0.0.0:9200/_cat/nodes?v"

# Attendre avant de créer un nouvel index
sleep 2

# Créer un index "cities" avec 2 shards et 2 replicas
echo "Création de l'index 'cities'..."
curl -s -X PUT 'http://localhost:9200/cities' -H 'Content-Type: application/json' -d '
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 2
  }
}'

# Attendre avant de vérifier les paramètres de l'index
sleep 2

# Vérifier les paramètres de l'index 'cities'
echo "Vérification des paramètres de l'index 'cities'..."
curl -s -X GET 'http://localhost:9200/cities/_settings' | jq

# Attendre avant d'ajouter un document
sleep 2

# Ajouter un document dans l'index 'cities'
echo "Ajout d'un document dans l'index 'cities'..."
curl -s -X POST 'http://localhost:9200/cities/_doc' -H 'Content-Type: application/json' -d '
{
  "city": "London",
  "country": "England"
}'

# Attendre avant de récupérer le document
sleep 2

# Récupérer le document ajouté
echo "Récupération du document ajouté..."
curl -s -X GET 'http://localhost:9200/cities/_doc/1' | jq

echo "Toutes les commandes ont été exécutées."
