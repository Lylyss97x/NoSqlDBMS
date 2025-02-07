# Pipeline d'Ingestion de Données pour le Traitement des Logs du Serveur Apache
Ce projet permet de mettre en place un pipeline d'ingestion de données afin de traiter les logs d'un serveur Apache à l'aide de Logstash, puis de visualiser les données dans Kibana. Ce projet offre une expérience pratique avec la pile Elastic (Elasticsearch, Logstash, Kibana) pour le traitement de données en temps réel.

Architecture du Projet
Voici l'architecture générale du projet :

```kotlin
Copier
├── data
│   └── apache_logs.txt
├── docker-compose.yml
├── logstash
│   └── logstash.conf

```

Prérequis
Docker et Docker Compose doivent être installés sur votre machine.
Étapes du Projet
1. Télécharger les Logs du Serveur Apache
Téléchargez un fichier de logs de serveur web Apache à partir du lien suivant (ou obtenez un fichier similaire) :

Sample Web Server Log

Enregistrez le fichier sous le nom apache_logs.txt dans un répertoire dédié à ce projet.

2. Configuration de Logstash
Dans le répertoire logstash, ouvrez le fichier logstash.conf dans un éditeur de texte et ajoutez la configuration suivante pour traiter les logs Apache :

```plaintext
Copier
input {
  file {
    path => "/data/apache_logs.txt"
    start_position => "beginning"
    sincedb_path => "/dev/null"
  }
}

filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}" }
  }
  date {
    match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    target => "@timestamp"
    remove_field => "timestamp"
  }
  geoip {
    source => "clientip"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "web_server_logs"
  }
}
Input : Utilise le plugin file pour lire les logs Apache depuis le fichier apache_logs.txt.
Filtre :
Grok : Utilise la correspondance COMBINEDAPACHELOG pour analyser les logs.
Date : Parse le champ timestamp au format approprié.
GeoIP : Utilise l'adresse IP du client pour ajouter des informations géographiques.
Output : Envoie les logs vers un index Elasticsearch nommé web_server_logs.
```

3. Mise à Jour de la Configuration Docker Compose
Modifie ton fichier docker-compose.yml pour inclure la nouvelle configuration de Logstash pour le traitement des logs Apache. Voici un exemple de configuration :

```yaml
Copier
logstash:
  image: logstash:7.6.2
  container_name: logstash
  hostname: logstash
  ports:
    - "5044:5044"
    - "9600:9600"
  volumes:
    - ./logstash/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    - /data/apache_logs.txt:/data/apache_logs.txt
  networks:
    - elk
  depends_on:
    - elasticsearch
```
Assurez-vous que le chemin vers apache_logs.txt correspond bien à l'endroit où vous avez stocké le fichier sur votre machine.

4. Démarrage du Stack ELK
Une fois que vous avez mis à jour votre fichier docker-compose.yml, redémarrez vos conteneurs Docker pour appliquer la nouvelle configuration :

```bash
Copier
docker-compose down
docker-compose up -d
```
Cette commande arrête et redémarre les conteneurs pour appliquer les changements.

5. Visualisation des Logs dans Kibana
Une fois que Logstash a commencé à ingérer les logs Apache, vous pouvez accéder à Kibana pour explorer et visualiser les données.

Ouvrez Kibana dans votre navigateur à l'adresse suivante :

```arduino
Copier
http://localhost:5601
```
Créez un index pattern pour les logs web Apache :

Accédez à Management > Index Patterns.
Cliquez sur Create index pattern et entrez web_server_logs* comme nom d'index.
Explorez les logs :

Allez dans l'onglet Discover dans la barre latérale gauche pour explorer les données indexées.
Vous pouvez filtrer et rechercher différents aspects des logs, comme les adresses IP, les codes de statut HTTP, etc.
6. Créer des Visualisations
Une fois que les logs sont indexés, vous pouvez créer des visualisations dans Kibana pour mieux comprendre les données.

Allez dans l'onglet Visualize dans la barre latérale gauche.
Cliquez sur le bouton Create visualization.
Sélectionnez le type de visualisation que vous souhaitez créer (par exemple, "Pie chart", "Vertical bar chart").
Choisissez le web_server_logs comme source de données.
Créez différentes visualisations basées sur les champs des logs, tels que :
Codes de réponse HTTP : Utilisez le champ response.
Top adresses IP des clients : Utilisez le champ clientip.
Ressources les plus fréquemment demandées : Utilisez le champ request.
Nombre de requêtes au fil du temps : Utilisez le champ @timestamp.
Répartition géographique des adresses IP des clients : Utilisez le champ geoip.location.
7. Vérification des Données dans Elasticsearch
Pour vérifier que les logs ont bien été ingérés dans Elasticsearch, vous pouvez utiliser une requête curl comme suit :

```bash
Copier
curl -X GET "localhost:9200/web_server_logs/_search?q=*" | jq
```
Cela vous permet de voir les logs dans Elasticsearch.
