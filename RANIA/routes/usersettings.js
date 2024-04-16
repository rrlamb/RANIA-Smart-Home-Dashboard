var express = require('express');
var router = express.Router();

var path = require("path");
var ap = path.join("Usersettings", "usersettings");

// Define route for /calendar
router.get('/', function(req, res, next) {
  res.render(ap, { title: 'Usersettings' }); 
});

module.exports = router;
