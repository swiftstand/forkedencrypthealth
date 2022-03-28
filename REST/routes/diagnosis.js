const express = require('express')
const router = express.Router()
const Diagnosis = require('../models/diagnosis')

// Get all
router.get('/', async (req, res) => {
    try {
        const reports = await Diagnosis.find()
        res.json(reports)
    } catch (err) {
        res.status(500).json({ message: err.message })
    }
})

// Get one
router.get('/:id', getDiagnosis, async (req, res) => {
    res.send(res.diagnosis)
})

// Create one
router.post('/', async (req, res) => {
    const diagnosis = new Diagnosis({
        name: req.body.name,
        labTests: req.body.labTests,
        date: req.body.date
    })
    try {
        const newDiagnosis = await diagnosis.save()
        res.status(201).json(newDiagnosis)
    } catch (err) {
        res.status(400).json({ message: err.message })
    }
})

// Update one
router.patch('/:id', async (req, res) => {
    if (req.body.name != null) {
        res.diagnosis.name = req.body.name
    }
    if (req.body.labTests != null) {
        res.diagnosis.labTests = req.body.labTests
    }
    if (req.body.date != null) {
        res.diagnosis.date = req.body.date
    }
    try {
        const updateDiagnosis = await res.diagnosis.save()
        res.json(updateDiagnosis)
    } catch (err) {
        res.status(400).json({ message: err.message })
    }
})

// Delete one
router.delete('/:id', getDiagnosis, async (req, res) => {
    try {
        await res.diagnosis.remove()
        res.json({ message: 'Deleted Diagnosis'})
    } catch (err) {
        res.status(500).json({ message: err.message })
    }

})

async function getDiagnosis(req, res, next) {
    let diagnosis
    try {
        diagnosis = await Diagnosis.findById(req.params.id)
        if (diagnosis == null) {
            return res.status(404).json({ message: 'Cannot find subscriber'})
        }
    } catch (err) {
        return res.status(500).json({ message: err.message})
    }
    res.diagnosis = diagnosis
    next()
}

module.exports = router