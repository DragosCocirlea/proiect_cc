const express = require('express');
const mongoose = require('mongoose');
const logger = require('morgan');
const createError = require('http-errors');
const bodyParser = require('body-parser');

const app = express();

// Middlewares
app.use(bodyParser.json());

// Import Routes
const trendsRouter = require('./routes/trends.js');

// Routes
app.use('/trends', trendsRouter);

app.use((req, res, next) => {
    next(createError(404));
});

app.use((err, req, res, next) => {
    console.log(req.url)
    res.status(err.status || 500);
    res.json({error: "Could not process request."});
})

// Connect to DB
mongoose.connect('mongodb://mongodb:27017/trends', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: true,
});

let db = mongoose.connection;
db.on('error', console.error.bind(console, "Connection error"));
db.on('open', () => {
    console.log("Connected to DB");
})

// Start listening
app.listen(5000);