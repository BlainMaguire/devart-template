var express  = require('express');
var app      = express();

var port = process.env.PORT || 8080;

app.configure(function() {
	app.use(express.logger('dev')); // log each request to the console for now
	app.use(express.static(__dirname + '/public'));
	app.use(express.bodyParser());
});

app.get('/api/options', function(req, res) {
    res.json([{ type : 'beziers', min_x: 4, max_x: 2, min_y: 4, max_y: 2 },
              { type : 'pointillism', colors : ['rgb(255,0,0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)']}]);
});

app.post('/api/currentoption', function(req, res) {
    var s = require('net').Socket();
    s.connect(8000);
    s.write(JSON.stringify(req.body));
    s.end();
    res.json({'status' : 'ok'});
});

app.get('*', function(req, res) {
    res.sendfile('./public/index.htm');
});

app.listen(port);
console.log("Server started on port: " + port);
