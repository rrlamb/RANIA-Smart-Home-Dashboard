var express = require('express');
var router = express.Router();

var path = require("path");
var dbp = path.join("Reminders", "reminders")
var dbpWizard = path.join("Wizards", "devices", "devices")

/* GET dashboard page. */
router.get('/', function (req, res, next) {
    res.render(dbp, { title: 'RANIA - Reminders' });
});

module.exports = router;
