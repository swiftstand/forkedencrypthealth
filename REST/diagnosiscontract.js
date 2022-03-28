'use strict';

const { Contract, Context } = require('fabric-contract-api')
const DiagnosisRecord = require('./diagnosisrecord.js')
const DiagnosisRecordList = require('./diagnosisrecordlist.js')

class DiagnosisRecordContext extends Context {

    constructor() {
        super()
        this.diagnosisRecordList = new DiagnosisRecordList(this)
    }
}

class DiagnosisRecordContract extends Contract {
    constructor() {
        super('DiagnosisRecordContract')
    }

    createContext() {
        return new DiagnosisRecordContext();
    }

    async init(ctx) {
        console.log('Instantiated the diagnosis record contract.')
    }

    async unknownTransaction(ctx) {
        throw new Error("Function name missing")
    }

    async createDiagnosisRecord(ctx, name, tests, date) {
        let record = DiagnosisRecord.createInstance(name, tests, date)
        await ctx.DiagnosisRecordList.addDiagRecord(record)
        return record.toBuffer()
    }

    async getDiagByKey(ctx, name, date) {
        const recordKey = DiagnosisRecord.makeKey([name, date])
        let record = await ctx.DiagnosisRecordList.getDiagRecord(recordKey)
        return JSON.stringify(record)
    }
    async transactionA(ctx, newValue) {
        let oldValue = await ctx.stub.getState(key);
        console.loc(`Old value: ${oldValue}`)
        console.loc(`New value: ${newValue}`)
        console.loc(`key: ${key}`)

        await ctx.stub.putState(key, Buffer.from(newValue))

        return Buffer.from(newValue.toString())
    }
}

module.export = DiagnosisRecordContract