#!/bin/bash

curl http://0.0.0.0:9200

sleep 5

curl http://0.0.0.0:9200/_cat/indices?v
