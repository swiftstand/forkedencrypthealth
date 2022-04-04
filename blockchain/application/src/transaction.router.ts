import { Contract } from '@hyperledger/fabric-gateway';
import express from 'express';
import { TextDecoder } from 'util';

export const transactionRouter = express.Router();
const utf8Decoder = new TextDecoder();

/** Get all Transactions.  **/
transactionRouter.get('/', async (req, res) => {
    console.log('\n--> Begin get all transactions <--')

    try {
        const contract = req.app.locals['contracts'].transactionContract as Contract;

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

    console.log('\n--> End get all transactions <--')
});

transactionRouter.get('/:transactionID', async(req, res) => {
    console.log('\n --> Begin get 1 transaction <--');

    const assetID = req.params.transactionID;
    console.log(`Getting assetID ${assetID}`);

    try {
        const contract = req.app.locals['contracts'].transactionContract as Contract;

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

    console.log('\n --> End get 1 transaction <--');
});

transactionRouter.post('/', async (req, res) => {
    console.log('\n --> Begin create transaction <--');

    try {
        const contract = req.app.locals['contracts'].transactionContract as Contract;

        const assetID = req.body.ID;
        const patientID = req.body.patientID;
        const amountPaid = req.body.amountPaid;
        const amountRemaining = req.body.amountRemaining;

        const commit = await contract.submitAsync(
            'CreateAsset',
            {
                arguments: [
                    assetID,
                    patientID,
                    amountPaid,
                    amountRemaining
                ]
            }
        );

        console.log(`*** Successfully submitted create transaction with assetID: ${assetID}`);
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
    console.log('\n --> End create transaction <--');
});

transactionRouter.patch('/:transactionID', async (req, res) => {
    const assetID = req.params.transactionID;
    console.log(`Updating asset: ${assetID}`);
    let updateAmount;
    if (req.body.amountPaid != null) {
        updateAmount = req.body.amountPaid;
        console.log(`Will pay ${updateAmount}`);
    } else {
        res.status(400).json({ messgae: 'You must provide the amountPaid key in body.' });
        return;
    }

    try {
        const contract = req.app.locals['contracts'].transactionContract as Contract;

        const commit = await contract.submitAsync(
            'PayMoney',
            {
                arguments: [
                    assetID,
                    updateAmount
                ]
            }
        );

        console.log(`*** Successfully submitted update transaction with assetID: ${assetID}`);
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
});