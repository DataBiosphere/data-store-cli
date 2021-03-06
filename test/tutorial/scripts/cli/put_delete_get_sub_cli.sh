#!/usr/bin/env bash

# Creates a sub based given a replica and a url
instance_info=$(dbio dss put-subscription --callback-url https://dcp-cli-tutorials-put-get-delete-sub.data.ucsc-cgp-redwood.org --replica aws) 

ID=`echo ${instance_info} | jq -r '.uuid'`

echo $ID

# Lists all of subs created
dbio dss get-subscriptions --replica aws

# List a sub
dbio dss get-subscription --replica aws --uuid $ID

# Deletes a sub based on a UUID
dbio dss delete-subscription --replica aws --uuid $ID
