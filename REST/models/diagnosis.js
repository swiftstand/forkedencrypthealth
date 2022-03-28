const mongoose = require('mongoose')

const diagnosisSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    labTests: {
        type: String,
        required: true
    },
    date: {
        type: Date,
        required: true,
        default: Date.now
    }
})

module.exports = mongoose.model('Diagnosis', diagnosisSchema)