import * as grpc from '@grpc/grpc-js';
import { 
    connect,
    Contract,
    Network,
    Gateway,
    Identity,
    Signer,
    signers
} from '@hyperledger/fabric-gateway';
import * as crypto from 'crypto';
import { promises as fs } from 'fs';
import * as path from 'path';
import * as config from './config';

// Org1 MSP ID
const mspId = config.mspID;

// Path to user private key directory.
const keyDirectoryPath = path.resolve(config.keyDirPath);

// Path to user certificate.
const certPath = path.resolve(config.certPath);

// Path to peer tls certificate.
const tlsCertPath = path.resolve(config.tlsCertPath);

// Gateway peer endpoint.
const peerEndpoint = config.peerEndpoint;

// Gateway peer SSL host name override.
const peerHostAlias = config.peerHostAlias;

export const createClientConnection = async (): Promise<grpc.Client> => {
    const client = await newGrpcConnection();
    return client
}

export const createGateway = async (
    client: grpc.Client,
    identity: Identity,
    signer: Signer
): Promise<Gateway> => {
    console.log('Configurting gateway');

    const gateway = connect({
        client,
        identity: identity,
        signer: signer,
    });
    // This was how the REST API did it w/ making Wallets
    // const gateway = new Gateway();
    // await gateway.connect(client,
        // {
        // identity: identity,
        // signer: signer,
        // eventHandlerOptions: {
            // commitTimeout: config.commitTimeout,
            // endorseTimeout: config.endorseTimeout
        // }
    // });
    return gateway;
}

async function newGrpcConnection(): Promise<grpc.Client> {
    const tlsRootCert = await fs.readFile(tlsCertPath);
    const tlsCredentials = grpc.credentials.createSsl(tlsRootCert);
    return new grpc.Client(peerEndpoint, tlsCredentials, {
        'grpc.ssl_target_name_override': peerHostAlias,
    });
}

export const newIdentity = async(): Promise<Identity> => {
    const credentials = await fs.readFile(certPath);
    return { mspId, credentials };
}

export const newSigner = async (): Promise<Signer> => {
    const files = await fs.readdir(keyDirectoryPath);
    const keyPath = path.resolve(keyDirectoryPath, files[0]);
    const privateKeyPem = await fs.readFile(keyPath);
    const privateKey = crypto.createPrivateKey(privateKeyPem);
    return signers.newPrivateKeySigner(privateKey);
}

export const getNetwork = async (
    gateway: Gateway, channelName: string
): Promise<Network> => {
    const network = await gateway.getNetwork(channelName);
    return network;
}

export const getContracts = async (
    network: Network
): Promise<{
    diagnosisContract: Contract;
    insuranceContract: Contract;
    transactionContract: Contract;
}> => {
    const diagnosisContract = network.getContract(config.diagnosisChainCode);
    const insuranceContract = network.getContract(config.insuranceChainCode);
    const transactionContract = network.getContract(config.transactionChainCode);
    return {
        diagnosisContract,
        insuranceContract,
        transactionContract
    };
}