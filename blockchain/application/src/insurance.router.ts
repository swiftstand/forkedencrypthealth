import { Contract } from '@hyperledger/fabric-gateway';
import express from 'express';
import { TextDecoder } from 'util';

export const insuranceRouter = express.Router();
const utf8Decoder = new TextDecoder();

/** Get all insurance.  **/
insuranceRouter.get('/', async (req, res) => {
    console.log('\n--> Begin get all insurances <--')

    try {
        const contract = req.app.locals['contracts'].insuranceContract as Contract;

        const resultBytes = await contract.evaluateTransaction('GetAllAssets');

        const resultJson = utf8Decoder.decode(resultBytes);
        const result = JSON.parse(resultJson);
        res.json(result);
    } catch (err) {
        if (err instanceof Error) {
            res.status(500).json({ message: err.message });
        } else {
            res.status(500).json({ message: String(err) });
        }
    }

    console.log('\n--> End get all insurances <--')
});

insuranceRouter.get('/:insuranceID', async(req, res) => {
    console.log('\n --> Begin get 1 insurance <--');

    const assetID = req.params.insuranceID;
    console.log(`Getting assetID ${assetID}`);

    try {
        const contract = req.app.locals['contracts'].insuranceContract as Contract;

        const resultBytes = await contract.evaluateTransaction('ReadAsset', assetID);

        const resultJson = utf8Decoder.decode(resultBytes);
        const result = JSON.parse(resultJson);
        res.json(result);
    } catch (err) {
        if (err instanceof Error) {
            res.status(500).json({ message: err.message });
        } else {
            res.status(500).json({ message: String(err) });
        }
    }

    console.log('\n --> End get 1 insurance <--');
});

insuranceRouter.post('/', async (req, res) => {
    console.log('\n --> Begin create insurance <--');

    try {
        const contract = req.app.locals['contracts'].insuranceContract as Contract;

        const assetID = req.body.ID;
        const patientID = req.body.patientID;
        const policyNumber = req.body.policyNumber;
        const requestedAmt = req.body.requestedAmt;
        const requestStatus = req.body.requestStatus;

        const commit = await contract.submitAsync(
            'CreateAsset',
            {
                arguments: [
                    assetID,
                    patientID,
                    policyNumber,
                    requestedAmt,
                    requestStatus
                ]
            }
        );

        console.log(`*** Successfully submitted create insurance with assetID: ${assetID}`);
        console.log('*** Waiting for transaction commit');

        const status = await(commit.getStatus());
        if (!status.successful) {
            console.log('*** Transaction failed.');
            res.status(status.code).json({
                message: `Transaction ${status.transactionId} failed to commit.`
            });
        } else {
            console.log('*** Transaction comitted successfully.');
            res.status(201).json(
                {
                    'assetID': assetID,
                    'txID': status.transactionId
                }
            );
        }
    } catch (err) {
        if (err instanceof Error) {
            res.status(500).json({ message: err.message });
        } else {
            res.status(500).json({ message: String(err) });
        }
    }
    console.log('\n --> End create insurance <--');
});

insuranceRouter.patch('/:insuranceID', async (req, res) => {
    const assetID = req.params.insuranceID;
    console.log(`Updating asset: ${assetID}`);

    let updateStatus;
    if (req.body.requestStatus != null) {
        updateStatus = req.body.requestStatus;
        console.log(`Will update status to ${updateStatus}`);
    } else {
        res.status(400).json({ message: 'You must provide requestStatus key in body.' });
        return;
    }
    try {
        const contract = req.app.locals['contracts'].insuranceContract as Contract;

        const commit = await contract.submitAsync(
            'UpdateStatus',
            {
                arguments: [
                    assetID,
                    updateStatus
                ]
            }
        );

        console.log(`*** Successfully submitted update insurance with assetID: ${assetID}`);
        console.log('*** Waiting for transaction commit');

        const status = await(commit.getStatus());
        if (!status.successful) {
            console.log('*** insurance failed.');
            res.status(status.code).json({
                message: `Transaction ${status.transactionId} failed to commit.`
            });
        } else {
            console.log('*** Transaction comitted successfully.');
            res.status(201).json(
                {
                    'assetID': assetID,
                    'txID': status.transactionId
                }
            );
        }
    } catch (err) {
        if (err instanceof Error) {
            res.status(500).json({ message: err.message });
        } else {
            res.status(500).json({ message: String(err) });
        }
    }
});