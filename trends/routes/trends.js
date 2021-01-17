const express = require('express');
const router = express.Router();
const Trend = require('../models/Trend');

router.get('/', async (req, res) => {
    Trend.find()
    .then(trends => {
        res.json(trends);
    })
    .catch(err => {
        console.log(err);
        res.status(500);
    })
})

router.get('/:haircutID', async (req, res) => {
    Trend.findById(req.params.haircutID)
    .then(trend => {
        res.json(trend);
    })
    .catch(err => {
        console.log(err);
        res.status(500);
    })
})

router.patch('/:haircutID', async (req, res) => {
    Trend.findByIdAndUpdate(
        req.params.haircutID,
        {$inc: {hits: 1}},
        {new: true}
    )
    .then(trend => {
        res.json(trend);
    })
    .catch(err => {
        console.log(err);
        res.status(500);
    })
})

module.exports = router;