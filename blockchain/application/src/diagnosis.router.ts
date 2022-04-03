import { Contract } from '@hyperledger/fabric-gateway';
import express from 'express';
import { TextDecoder } from 'util';

export const diagnosisRouter = express.Router();
const utf8Decoder = new TextDecoder();

/** Get all diagnosis.  **/
diagnosisRouter.get('/', async (req, res) => {
    console.log('\n--> Begin get all diagnosiss <--')

    try {
        const contract = req.app.locals['contracts'].diagnosisContract as Contract;

        const resultBytes = await contract.evaluateTransaction('GetAllAssets');

        const resultJson = utf8Decoder.decode(resultBytes);
        const result = JSON.parse(resultJson);
        const parsedResult = result.map((user: any) => {
            user['Perscriptions'] = JSON.parse(user['Perscriptions']);
            user['TestsRequested'] = JSON.parse(user['TestsRequested']);
            return user;
        });
        res.json(parsedResult);
    } catch (err) {
        if (err instanceof Error) {
            res.status(500).json({ message: err.message });
        } else {
            res.status(500).json({ message: String(err) });
        }
    }

    console.log('\n--> End get all diagnosiss <--')
});

diagnosisRouter.get('/:diagnosisID', async(req, res) => {
    console.log('\n --> Begin get 1 diagnosis <--');

    const assetID = req.params.diagnosisID;
    console.log(`Getting assetID ${assetID}`);

    try {
        const contract = req.app.locals['contracts'].diagnosisContract as Contract;

        const resultBytes = await contract.evaluateTransaction('ReadAsset', assetID);

        const resultJson = utf8Decoder.decode(resultBytes);
        const result = JSON.parse(resultJson);
        result['Perscriptions'] = JSON.parse(result['Perscriptions']);
        result['TestsRequested'] = JSON.parse(result['TestsRequested']);
        res.json(result);
    } catch (err) {
        if (err instanceof Error) {
            res.status(500).json({ message: err.message });
        } else {
            res.status(500).json({ message: String(err) });
        }
    }

    console.log('\n --> End get 1 diagnosis <--');
});

diagnosisRouter.post('/', async (req, res) => {
    console.log('\n --> Begin create diagnosis <--');

    try {
        const contract = req.app.locals['contracts'].diagnosisContract as Contract;

        const assetID = req.body.ID;
        const patientID = req.body.patientID;
        const doctorID = req.body.doctorID;
        const diagnosis = req.body.diagnosis;
        const testsRequested = JSON.stringify(req.body.testsRequested);
        const perscriptions = JSON.stringify(req.body.perscriptions);

        const commit = await contract.submitAsync(
            'CreateAsset',
            {
                arguments: [
                    assetID,
                    patientID,
                    doctorID,
                    diagnosis,
                    testsRequested,
                    perscriptions
                ]
            }
        );

        console.log(`*** Successfully submitted create diagnosis with assetID: ${assetID}`);
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
    console.log('\n --> End create diagnosis <--');
});

diagnosisRouter.patch('/:diagnosisID', async (req, res) => {
    console.log('\n --> Begin update diagnosis <--');

    const assetID = req.params.diagnosisID;
    console.log(`Updating asset: ${assetID}`);

    const patientID = req.body.patientID;
    const doctorID = req.body.doctorID;
    const diagnosis = req.body.diagnosis;
    const testsRequested = req.body.testsRequested;
    const perscriptions = req.body.perscriptions;

    try {
        const contract = req.app.locals['contracts'].diagnosisContract as Contract;

        const commit = await contract.submitAsync(
            'UpdateAsset',
            {
                arguments: [
                    assetID,
                    patientID,
                    doctorID,
                    diagnosis,
                    testsRequested,
                    perscriptions
                ]
            }
        );

        console.log(`*** Successfully submitted update diagnosis with assetID: ${assetID}`);
        console.log('*** Waiting for transaction commit');

        const status = await(commit.getStatus());
        if (!status.successful) {
            console.log('*** diagnosis failed.');
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

    console.log('\n --> End update diagnosis <--');
});