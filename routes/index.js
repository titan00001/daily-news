var express = require('express');
var router = express.Router();

const {getNews, getFilteredNews, runScrapper } = require("../public/data/getNews")

/* GET home page. */
router.get('/', function(req, res, next) {

    news = getNews('India')
    res.render('index', { title: 'Daily News', newsJson: news });
  
});

router.get('/refresh', function(req, res){
    runScrapper()
    res.redirect('/')
})

router.get('/politics', function(req, res, next) {

    news = getNews('India')
    news = getFilteredNews(news["timesofindia.indiatimes.com"], ["india", "elections", "world", "business", "nri"])
    res.render('index', { title: 'Political News', newsJson: news });

})

router.get('/city', function(req, res, next) {

  news = getNews('India')
  res.render('index', { title: 'City News', newsJson: news["timesofindia.indiatimes.com"]["city"] });

})

router.get('/coupon', function(req, res, next) {

  news = getNews('India')
  res.render('index', { title: 'Coupon News', newsJson: news["www.coupondunia.in"] });

})



router.get('/china', function(req, res, next) {

  news = getNews('China')
  res.render('index', { title: 'Global-Times', newsJson: news });

})

router.get('/US', function(req, res, next) {

  news = getNews('US')
  res.render('index', { title: 'USA-Today', newsJson: news });

})

router.get('/EU', function(req, res, next) {

  news = getNews('EU')
  res.render('index', { title: 'Euro-news', newsJson: news });

})

module.exports = router;
