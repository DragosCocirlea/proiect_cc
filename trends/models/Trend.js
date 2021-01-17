const mongoose = require('mongoose');

const TrendSchema = mongoose.Schema({
    name: String,
    description: String,
    hits: Number
})

module.exports = mongoose.model('Trends', TrendSchema);