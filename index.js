var path = require('path');
var url = require('url');
const {spawn} = require('child_process');
var fs = require('fs');
const express = require('express')
const app = express()
const port = 8080
var events = require('events');
const Queue = require('bull');
var redis = require('redis');
var client = redis.createClient();

var eventEmitter = new events.EventEmitter();

var count = 0

const queueScript = new Queue('queueScript');

queueScript.process(async job => {
    eventEmitter.emit('generateReport', job.res);
  })

var generateReport = function(res){
    var dataToSend;
    const python = spawn('python', ['main.py']);

    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.slice(0, -2); 
    });

    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        var file = fs.createReadStream('./' + dataToSend+'.pdf');
        var stat = fs.statSync('./' + dataToSend+'.pdf');
        res.setHeader('Content-Length', stat.size);
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', 'attachment; filename='+dataToSend+'.pdf');
        file.pipe(res);
        
    });
}

eventEmitter.on('generateReport', generateReport);

app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
})

app.post('/generate-report', function (req, res) {
    queueScript.add(res);
    
    //res.send("Done");
})

app.listen(8080);

/*http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
  fs.readFile(filename, function(err, data) {
    if (err) {
      res.writeHead(404, {'Content-Type': 'text/html'});
      return res.end("404 Not Found");
    } 
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(data);
    return res.end();
  });
}).listen(8080);*/