var app = require('express')(),
    server = require('http').createServer(app),
    io = require('socket.io').listen(server),
    ent = require('ent'), // Permet de bloquer les caractères HTML (sécurité équivalente à htmlentities en PHP)
    fs = require('fs');
    require('events').EventEmitter.prototype._maxListeners = 0;

var jf = require('jsonfile'); //jsonfile module


// Chargement de la page index.html
app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

io.sockets.on('connection', function(socket) {
    setTimeout(function(){
    jf.readFile("listeresident.json", function(err, data) { //if change detected read the dat.json
        var data = data; //store in a var
        console.log('data send ') //just for debugging
        socket.volatile.emit('init', data); //emit to all clients
        });
    }, 100);

    fs.watch("listeresident.json", function(event, fileName) { //watching my  data.json file for any changes
        //NOTE: fs.watch returns event twice on detecting change due to reason that editors fire 2 events --- there are workarounds for this on stackoverflow

        jf.readFile("listeresident.json", function(err, data) { //if change detected read the sports.json

            var data = data; //store in a var
           /* console.log(data) //just for debugging*/
            socket.volatile.emit('notification', data); //emit to all clients
        });

        // Dès qu'on reçoit un message, on récupère le pseudo de son auteur et on le transmet aux autres personnes
        socket.on('message', function (message) {
            message = ent.encode(message);
            socket.broadcast.emit('message', {pseudo: socket.pseudo, message: message});
        });
    });
});



server.listen(3000, function() { //listen to 3000
console.log('listening on *:3000');
});

