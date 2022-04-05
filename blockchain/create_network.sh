#!/bin/bash
. .env

# Move to the network dir and set a trap to move back if we exit
pushd network > /dev/null
trap "popd > /dev/null" EXIT

# Create network and run all 3 CCs
bash network.sh up createChannel -c ${CHANNEL_NAME} -ca
bash network.sh deployCC -c ${CHANNEL_NAME} -ccn ${DIAGNOSIS_CC_NAME} -ccp ${DIAGNOSIS_CC_PATH} -ccl typescript
bash network.sh deployCC -c ${CHANNEL_NAME} -ccn ${INSURANCE_CC_NAME} -ccp ${INSURANCE_CC_PATH} -ccl typescript
bash network.sh deployCC -c ${CHANNEL_NAME} -ccn ${TRANSACTION_CC_NAME} -ccp ${TRANSACTION_CC_PATH} -ccl typescript
