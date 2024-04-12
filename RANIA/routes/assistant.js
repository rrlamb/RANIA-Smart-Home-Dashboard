var express = require("express");
var router = express.Router();

var path = require("path");
var ap = path.join("Assistant", "assistant");

/* GET assistant page. */
router.get("/", function (req, res, next) {
  res.render(ap, { title: "Assistant" });
});

module.exports = router;
