

function runScrapper() { 
      
    // Use child_process.spawn method from  
    // child_process module and assign it 
    // to variable spawn 
    var spawn = require("child_process").spawn; 
      
    // Parameters passed in spawn - 
    // 1. type_of_script 
    // 2. list containing Path of the script 
    //    and arguments for the script  
      
    // E.g : http://localhost:3000/name?firstname=Mike&lastname=Will 
    // so, first name = Mike and last name = Will 
    var scrapper = spawn('py', ["public/data/Scrapper.py"]); 
  
    // Takes stdout data from script which executed 
    // with arguments and send this data to res object

    scrapper.stderr.pipe(process.stderr)

    scrapper.stdout.pipe(process.stdout)

    return 1
} 


function getNews(){

    var data = {}

    if(runScrapper() === 1){
        data = require("./ToiNews.json")
    }
    return data
}

function deleteNews(news, topicToDelete){

    for(key in news) {
        if(topicToDelete.includes(key)) {
            delete news[key];
        }
    }
    return news
}

function getFilteredNews(news, topicRequired){

    topicInNews = Object.keys(news)

    for(key of topicRequired) {
        topicInNews = topicInNews.filter(item => {
            return item !== key
        });
    }

    return deleteNews(news, topicInNews)

}

module.exports = { getNews, getFilteredNews };