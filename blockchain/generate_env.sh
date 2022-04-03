#!/bin/bash
gen_env() {
    echo "MSP_ID=Org1MSP"
    echo "CHANNEL_NAME=blockchain-channel"
    echo "PEER_ENDPOINT=localhost:7051"
    echo "PEER_HOST_ALIAS=peer0.org1.example.com"
    echo "REST_API_PORT=10147"
    echo ""
    MAIN_DIR=$(pwd)
    CRYPTO_PATH=${MAIN_DIR}/network/organizations/peerOrganizations/org1.example.com
    echo "KEY_DIRECTORY_PATH=${CRYPTO_PATH}/users/User1@org1.example.com/msp/keystore"
    echo "CERT_PATH=${CRYPTO_PATH}/users/User1@org1.example.com/msp/signcerts/cert.pem"
    echo "TLS_CERT_PATH=${CRYPTO_PATH}/peers/peer0.org1.example.com/tls/ca.crt"
    echo ""
    echo "DIAGNOSIS_CC_NAME=diagnosis_cc"
    echo "DIAGNOSIS_CC_PATH=$(realpath ${MAIN_DIR}/diagnosis_chaincode)"
    echo "INSURANCE_CC_NAME=insurance_cc"
    echo "INSURANCE_CC_PATH=$(realpath ${MAIN_DIR}/insurance_chaincode)"
    echo "TRANSACTION_CC_NAME=transaction_cc"
    echo "TRANSACTION_CC_PATH=$(realpath ${MAIN_DIR}/transaction_chaincode)"
}
gen_env | tee .env application/.env
