// models/reminder.js (or wherever your model is defined)
const mongoose = require('mongoose');

const reminderSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  date: {
    type: Date,
    required: true
  },
  time: {
    type: String,
    required: true
  }
});

module.exports = mongoose.model('Reminder', reminderSchema);
