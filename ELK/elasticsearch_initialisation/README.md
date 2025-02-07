# 📝 Explication des Étapes du Script Init.sh :
Le script contient plusieurs étapes avec des temps d'attente entre chaque commande pour assurer que chaque action se termine correctement avant de passer à la suivante. Voici le détail des commandes exécutées :

1. Vérification de l'état du cluster :
La première commande interroge l'état général du cluster Elasticsearch en utilisant l'API _cluster/health :

```bash
Copier
curl -s 0.0.0.0:9200/_cluster/health | jq
```
Elle retourne des informations telles que l'état du cluster, le nombre de nœuds, et les indices présents.

2. Vérification des nœuds du cluster :
La deuxième étape récupère la liste des nœuds du cluster avec l'API _cat/nodes :

```bash
Copier
curl -s -X GET "http://0.0.0.0:9200/_cat/nodes?v"
```

Cela vous permet de vérifier les nœuds actifs et leur état.

3. Création d'un index 'cities' :
Ensuite, un index nommé cities est créé avec 2 shards et 2 réplicas pour garantir la redondance et la performance des recherches :

```bash
Copier
curl -s -X PUT 'http://localhost:9200/cities' -H 'Content-Type: application/json' -d '
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 2
  }
}'
```

4. Vérification des paramètres de l'index 'cities' :
Après la création de l'index, le script interroge les paramètres de cet index pour vérifier les configurations appliquées :

```bash
Copier
curl -s -X GET 'http://localhost:9200/cities/_settings' | jq
```

Cela permet de s'assurer que l'index a bien été créé avec les bonnes configurations.

5. Ajout d'un document dans l'index 'cities' :
Un document représentant une ville est ajouté à l'index cities :

```bash
Copier
curl -s -X POST 'http://localhost:9200/cities/_doc' -H 'Content-Type: application/json' -d '
{
  "city": "London",
  "country": "England"
}'
```

Le document contient le nom de la ville "London" et le pays "England".

6. Récupération du document ajouté :
Enfin, le script récupère le document ajouté à l'index et l'affiche :

bash
Copier
curl -s -X GET 'http://localhost:9200/cities/_doc/1' | jq
Cela permet de vérifier que le document a bien été indexé et est accessible via Elasticsearch.
