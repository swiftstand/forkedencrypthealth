'use strict';

const StateList = require('./tmp/statelist.js')

const DiagnosisRecord = require('./diagnosisrecord.js')

class DiagnosisRecordList extends StateList {
    constructor(ctx) {
        super(ctx, 'DiagnosisRecordList')
        this.use(DiagnosisRecord)
    }

    async addDiagRecord(record) {
        return this.addState(record)
    }

    async getDiagRecord(recordKey) {
        return this.getState(recordKey)
    }

    async updateDiagRecord(record) {
        return this.updateState(record)
    }

}

module.exports = DiagnosisRecordList