#!/bin/sh

# shellcheck disable=SC2154
# shellcheck disable=SC2034
contur=$1
rm -rf .env

# shellcheck disable=SC2050
if [ "$contur" = "Test" ]; then
  echo "$contur"
  # shellcheck disable=SC2129
  echo CONTOUR=Test >>.env
  echo API_ENTRYPOINT='python -m unittest tests/test.py -vv' >>.env
elif
  [ "$contur" = "Local" ]
then
  echo "$contur"
  # shellcheck disable=SC2129
  echo CONTOUR=Local >>.env
else
  echo No countur settings "$contur"
fi
