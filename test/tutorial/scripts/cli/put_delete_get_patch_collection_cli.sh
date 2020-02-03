#!/usr/bin/env bash

info_instance=$(dbio dss put-collection --uuid fff01947-bf94-43e9-86ca-f6ff6ae45d2c --description foo --details {} --version 2018-09-17T161441.564206Z --replica aws --name bar --contents '{"path": "https://dss.dev.ucsc-cgp-redwood.org/v1/bundles/ff818282-9735-45fa-a094-e9f2d3d0a954?version=2019-08-06T170839.843085Z&replica=aws", "version": "2019-08-06T170839.843085Z", "type": "bundle", "uuid": "ff818282-9735-45fa-a094-e9f2d3d0a954"}')

ID=`echo ${info_instance} | jq -r '.uuid'`
VERSION=`echo ${info_instance} | jq -r '.version'`

dbio dss get-collections

dbio dss patch-collection --replica aws --uuid $ID --verison $VERSION

dbio dss get-collection --replica aws --uuid $ID

dbio dss delete-collection --replica aws --uuid $ID
