#!/bin/bash

docker-compose up -d
sleep 10
docker-compose exec logstash bin/logstash --config.test_and_exit -f /usr/share/logstash/pipeline/logstash.conf
sleep 5

curl -X GET "0.0.0.0:9200/csv-data/_search?q=*" | jq
