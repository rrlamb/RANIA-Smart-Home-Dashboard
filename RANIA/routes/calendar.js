var express = require('express');
var router = express.Router();
var path = require("path");
var ap = path.join("Calendar", "calendar");


// Define route for /calendar
router.get('/', function(req, res, next) {
 res.render(ap, { title: 'Calendar' });
});

// Fetch Reminders Endpoint
router.get('/getReminders', async (req, res) => {
    try {
      const reminders = await Reminder.find();
      res.json(reminders);
    } catch (err) {
      console.error(err);
      res.status(500).send('Server Error');
    }
  });
  
module.exports = router;