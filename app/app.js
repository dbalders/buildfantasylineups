// var http = require('http');
var express = require('express');
var app = express();
var fs = require("fs");

app.use(express.static(__dirname + '/../'));

app.get('/listUsers', function(req, res) {
    fs.readFile(__dirname + "/" + "users.json", 'utf8', function(err, data) {
        console.log(data);
        res.end(data);
    });
})

app.get('/fdPlayers', function(req, res) {
    fs.readFile(__dirname + "/" + "../assets/json/fddata.json", 'utf8', function(err, data) {
        console.log(data);
        res.end(data);
    });
})

app.get('/blank', function(req, res) {
    fs.readFile(__dirname + "/" + "../assets/json/blank.json", 'utf8', function(err, data) {
        console.log(data);
        res.end(data);
    });
})

app.get('/optimalLastFive', function(req, res) {
    fs.readFile(__dirname + "/" + "../assets/json/optimalLastFive.json", 'utf8', function(err, data) {
        console.log(data);
        res.end(data);
    });
})

app.get('/optimalAVG', function(req, res) {
    fs.readFile(__dirname + "/" + "../assets/json/optimalAVG.json", 'utf8', function(err, data) {
        console.log(data);
        res.end(data);
    });
})

app.get('/optimalRotogrinders', function(req, res) {
    fs.readFile(__dirname + "/" + "../assets/json/optimalRotogrinders.json", 'utf8', function(err, data) {
        console.log(data);
        res.end(data);
    });
})

app.get('/fdFinalData', function(req, res) {
    fs.readFile(__dirname + "/" + "../assets/json/fdFinalData.json", 'utf8', function(err, data) {
        console.log(data);
        res.end(data);
    });
})

var server = app.listen(8000, function() {

    var host = server.address().address
    var port = server.address().port

    console.log("Fantsy Lineups app listening at http://%s:%s", host, port)

})
