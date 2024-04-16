var express = require('express');
var router = express.Router();

var path = require("path");
var dbp = path.join("Homepage", "homepage")
var dbpWizard = path.join("Wizards", "devices", "devices")

/* GET dashboard page. */
router.get('/', function (req, res, next) {
  res.render(dbp, { title: 'RANIA - Homepage' });
});

module.exports = router;