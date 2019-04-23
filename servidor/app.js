'use strict'

const express = require('express');
const {PythonShell} = require("python-shell");
const socketIO=require('socket.io');

//Configuracion del sevidor
const app = express();

app.use(express.static(__dirname + '/cliente'));

var server = app.listen(3000, ()=> console.log('listening on port 3000...'));

//Configuracion del socket
var io = socketIO(server);

io.on('connection', function(socket){
	console.log("conexión establecida");

	socket.on('request', function(data){
		console.log(data);
		pythonScript(data);
	});

});

//Comunicacion con python
function pythonScript(arg){

	var options = {
		mode: 'text',
		encoding: 'utf8',
		pythonOptions: ['-u'],
		scriptPath: './servidor/src', //la ruta cambia, ésta es para ejecutarla de la carpeta raiz del proyecto
		args: ["-t",arg.split(",")[0], "-a",arg.split(",")[1]], //"123456078 123456780"
		pythonPath: 'python' //colocar la propia ruta de python
	};


	var pythonCode = new PythonShell('main.py', options);
	pythonCode.on('message', function (message){
		console.log(message);
		io.emit('response', message);
	});
}




