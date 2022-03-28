require('dotenv').config()
const express = require('express')
const mongoose = require('mongoose')

const app = express()

mongoose.connect(process.env.DATABASE_URL, { useNewUrlParser: true })
const db = mongoose.connection
db.on('error', (error) => console.error(error))
db.once('open', () => console.log('Connected to Database'))

app.use(express.json())

const diagnosisRouter = require('./routes/diagnosis')
app.use('/diagnosis', diagnosisRouter)

app.listen(10000, () => console.log('Server Started'))