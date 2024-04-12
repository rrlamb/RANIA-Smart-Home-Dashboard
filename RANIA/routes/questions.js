var express = require("express");
var router = express.Router();

var path = require("path");
var ap = path.join("Questions", "questions");

/* GET assistant page. */
router.get("/", function (req, res, next) {
  res.render(ap, { title: "Questions" });
});

module.exports = router;
