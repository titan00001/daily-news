// for adding python-scrapper:
// 1. Add script in python-scripts folder
// 2. Update the list in for loop
// 3. Add case in switch
// 4. Change the path name of json file to public/data/MyJsonFile.json
// 5. To change frontend Add link to navbar in header in index.ejs

function runScrapper() { 
      
    // Use child_process.spawn method from  
    // child_process module and assign it 
    // to variable spawn 

    // var spawn = require("child_process").spawn; 
      
    // Parameters passed in spawn - 
    // 1. type_of_script 
    // 2. list containing Path of the script 
    //    and arguments for the script  
      
    // E.g : http://localhost:3000/name?firstname=Mike&lastname=Will 
    // so, first name = Mike and last name = Will 

    for (script of ['Scrapper.py', 'usa-today-scrapper.py', 'euronews-scrapper.py', 'Global-times-china-scrapper.py', 'money-control.py']) {

        console.log(script)

        var spawn = require("child_process").spawn; 
        scriptPath = 'public/python-scripts/' + script;

        var scrapper = spawn('py', [scriptPath]); 
  
        // Takes stdout data from script which executed 
        // with arguments and send this data to res object

        scrapper.stderr.pipe(process.stderr)

        scrapper.stdout.pipe(process.stdout)
    }
    

    return 1
} 

// european-news.json   global-times.json   usa-today.json

function getNews(country){

    var data = {}

    switch (country) {
        case 'India': data = require("./ToiNews.json");
            break;
        
        case 'China': data = require("./global-times.json");
        break;

        case 'US': data = require("./usa-today.json");
            break;

        case 'EU': data = require("./european-news.json");
            break;

        case 'Economics': data = require('./money-control-economic.json')
            break;
    
        default:
            break;
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

module.exports = { getNews, getFilteredNews, runScrapper };