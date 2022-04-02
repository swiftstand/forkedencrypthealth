import * as config from './config';
import express from 'express';
import helmet from 'helmet';
import { diagnosisRouter } from './diagnosis.router';
import { insuranceRouter } from './insurance.router';
import { transactionRouter } from './transaction.router';
import {
    createGateway,
    createClientConnection,
    newIdentity,
    newSigner,
    getNetwork,
    getContracts,
} from './fabric';

async function main(): Promise<void> {
    const app = express();
    app.use(express.json());

    console.log(`Running in ${process.env.NODE_ENV}`);
    if (process.env.NODE_ENV === 'producion') {
        app.use(helmet());
    }

    app.use('/diagnosis', diagnosisRouter);
    app.use('/insurance', insuranceRouter);
    app.use('/transactions', transactionRouter);

    const grpcConnection = await createClientConnection();
    const identity = await newIdentity();
    const signer = await newSigner();
    const gateway = await createGateway(
        grpcConnection, identity, signer
    );
    const network = await getNetwork(
        gateway, config.channelName
    );
    const contracts = await getContracts(network);

    app.locals['contracts'] = contracts;

    app.listen(config.port, () => {
        console.log('REST server started on port: %d', config.port)
    });
}

main().catch(error => {
    console.error('ERROR WHEN RUNNING APPLICATION: ', error);
    process.exitCode = 1;
})
