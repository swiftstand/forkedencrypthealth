'use strict';

const State = require('./tmp/state.js')

class DiagnosisRecord extends State {

    constructor(obj) {
        super(DiagnosisRecord.getClass(), [obj.name, obj.date])
        Object.assign(this, obj)
    }
    getName() { return this.name }
    setName(newName) { this.name = newName }
    getLabTest() { return this.labTest }
    setLabTest(newLabTest) { this.labTest = newLabTest }
    getDate() { return this.date }
    setDate(newDate) { this.date = newDate }

    static fromBuffer(buffer) {
        return DiagnosisRecord.deseralize(Buffer.from(JSON.parse(buffer)))
    }

    toBuffer() {
        return Buffer.from(JSON.stringify(this))
    }

    static deserialize(data) {
        return State.deserializeClass(data, DiagnosisRecord)
    }

    static createInstance(name, tests, date) {
        return new DiagnosisRecord({name, tests, date})
    }

    static getClass() {
        return 'DiagnosisRecord'
    }

}

module.exports = DiagnosisRecord