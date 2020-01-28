var express = require('express');
var router = express.Router();

const {getNews, getFilteredNews } = require("../public/data/getNews")

/* GET home page. */
router.get('/', function(req, res, next) {

    news = getNews()
    res.render('index', { title: 'Daily News', newsJson: news });
  
});

router.get('/politics', function(req, res, next) {

    news = getNews()
    news = getFilteredNews(news["timesofindia.indiatimes.com"], ["india", "elections", "world", "business", "nri"])
    res.render('index', { title: 'Political News', newsJson: news });

})

router.get('/city', function(req, res, next) {

  news = getNews()
  res.render('index', { title: 'City News', newsJson: news["timesofindia.indiatimes.com"]["city"] });

})

module.exports = router;

