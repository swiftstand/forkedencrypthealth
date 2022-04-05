#!/bin/bash
. .env

pushd application > /dev/null
trap "popd > /dev/null" EXIT

[[ ! -d "node_modules" ]] && npm i || :

npm run prepare && npm start
