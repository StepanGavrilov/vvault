#!/bin/sh

# shellcheck disable=SC2034
contur=$1
./env.sh "$contur" >>.env &
# shellcheck disable=SC2050

if [ "$contur" = "Local" ]; then
  echo "$contur"
  docker-compose -f docker-compose.yml up --build

elif [ "$contur" = "Test" ]; then
  echo "$contur"
  docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build --exit-code-from vault-test-app
  docker-compose -f docker-compose.yml -f docker-compose.test.yml down --remove-orphans

else
  echo No countur settings "$contur"

fi
