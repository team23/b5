#!/usr/bin/env bash

b5:module_load docker_django

DOCKER_DJANGO_SOLR_SERVICE="solr"
DOCKER_DJANGO_SOLR_SCHEMA_PATH="${DOCKER_DATA_PATH}/${DOCKER_DJANGO_SOLR_SERVICE}/collection1/conf/schema.xml"

docker_django_solr:update() {
    DOCKER_RUN_NOTTY=yes docker_django:run build_solr_schema > "${DOCKER_DJANGO_SOLR_SCHEMA_PATH}"
}
