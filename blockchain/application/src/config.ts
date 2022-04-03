import * as env from 'env-var';

/**
 * The port for the REST API to listen on
 */
export const port = env
    .get('REST_API_PORT')
    .required()
    .asPortNumber();

/**
 * The channel name to listen on
 */
export const channelName = env
    .get('CHANNEL_NAME')
    .required()
    .asString();

/**
 * The chaincode name for our transaction contract
 */
export const transactionChainCode = env
    .get('TRANSACTION_CC_NAME')
    .required()
    .asString();

/**
 * The chaincode name for our diagnosis contract
 */
export const diagnosisChainCode = env
    .get('DIAGNOSIS_CC_NAME')
    .required()
    .asString();

/**
 * The chaincode name for our insurance contract
 */
export const insuranceChainCode = env
    .get('INSURANCE_CC_NAME')
    .required()
    .asString();

/**
 * The mspID for org 1
 */
export const mspID = env
    .get('MSP_ID')
    .required()
    .asString();

/**
 * Path to key dir for org1
 */
export const keyDirPath = env
    .get('KEY_DIRECTORY_PATH')
    .required()
    .asString();

export const certPath = env
    .get('CERT_PATH')
    .required()
    .asString();

export const tlsCertPath = env
    .get('TLS_CERT_PATH')
    .required()
    .asString();

export const peerEndpoint = env
    .get('PEER_ENDPOINT')
    .required()
    .asString();

export const peerHostAlias = env
    .get('PEER_HOST_ALIAS')
    .required()
    .asString();

console.log(`diagnosisChainCodeName:     ${diagnosisChainCode}`);
console.log(`insuranceChainCodeName:     ${insuranceChainCode}`);
console.log(`transactionChainCodeName:   ${transactionChainCode}`);
console.log(`channelName:       ${channelName}`);
console.log(`mspId:             ${mspID}`);
console.log(`keyDirectoryPath:  ${keyDirPath}`);
console.log(`certPath:          ${certPath}`);
console.log(`tlsCertPath:       ${tlsCertPath}`);
console.log(`peerEndpoint:      ${peerEndpoint}`);
console.log(`peerHostAlias:     ${peerHostAlias}`);
console.log(`REST API port:     ${port}`)