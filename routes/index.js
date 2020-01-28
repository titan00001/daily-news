var express = require('express');
var router = express.Router();

const getTOINews = require("../public/data/getNews")

/* GET home page. */
router.get('/', function(req, res, next) {

    news = getTOINews()
    res.render('index', { title: 'Daily News', newsJson: news });
  
});

module.exports = router;

