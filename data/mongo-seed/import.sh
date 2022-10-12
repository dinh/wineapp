#!/bin/bash

set -e

# wait until mongodb is ready
until mongo --host mongodb --eval "db.version()"; do
  >&2 echo "mongodb is unavailable - sleeping"
  sleep 1
done

>&2 echo "mongodb is up - executing command"

# Don't import the data if the winedb exists
mongo_indexof_db=$(mongo --host mongodb --quiet --eval 'db.getMongo().getDBNames().indexOf("winedb")')
echo $mongo_indexof_db
if [ $mongo_indexof_db -ne "-1" ]; then
    echo "MongoDB database exists"
    echo "Aborting"
else
    echo "Creating the winedb database"
    echo "Creating the review collection"
    echo "IMPORTING COLLECTION"
    mongoimport --host mongodb --db winedb --collection review --type json --file /mongo-seed/winemag-data-130k-v2.json --jsonArray
fi
echo "CLEANING UP"
echo DONE IMPORTING
