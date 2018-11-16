var data = {
	"Boston": .3,
	"technology": .8,
	"Kristin": .2,
	"swimming": .9,
	"asd": .4,
	"weee": .2,
	"qqq": .6,
	"ssss": .1,

	"11": .1,
	"as22d": .2,
	"we33ee": .3,
	"qqq44": .4,
	"ss55ss": .5,

};

var circles = [];

function distance(x1, y1, x2, y2) {return Math.sqrt( Math.pow((x1-x2), 2) + Math.pow((y1-y2), 2) );}


function markGrid(grid, diam, x, y) {
	var topx = x - int(diam / 2);
	var topy = y - int(diam / 2);

	for (var i = 0; i < diam; i++) {
		for (var j = 0; j < diam; j++){
			if (distance(i+topx,j+topy, x, y) <= int(diam/2)){

				// console.log(i+topx);
				// console.log(j+topy);
				grid[i+topx][j+topy] = 1;
			}
		}
	}
}

function doesItFitGrid(grid, diam, x, y) {

	if (x < (diam / 2)) {return false};
	if (y < (diam / 2)) {return false};

	var topx = x - int(diam / 2);
	var topy = y - int(diam / 2);

	for (var i = 0; i < diam; i++) {
		for (var j = 0; j < diam; j++){
			if (distance(i+topx,j+topy, x, y) <= int(diam/2)){
				if (i+topx >= 400) {return false};
				if (j+topy >= 400) {return false};
				if (grid[i+topx][j+topy] == 1) {return false};
			}
		}
	}
	return true;
}

function setup() {
	var width = 400;
	var height = 400;
	var canvas = createCanvas(width, height);
	noLoop();
	var keywords = document.getElementById("p5-canvas").getAttribute("value");

	var sals = document.getElementById("info").getAttribute("value");
	data = {};
	console.log(saliences);

	canvas.parent('p5-canvas');

	var grid = new int(400);

	for (var i = 0; i < 400; i++) {
	  grid[i] = new int(400);
	}

	for (var x = 0; x < 400; x++) {
		for (var y = 0; y < 400; y++){
			grid[x][y] = 0;
		}
	}
	var words = keywords.split(", ");
	var saliences = sals.split(", ");
	for (var k = 0; k < words.length; k++) {
		if (words[k][0] == "[") {
			words[k] = words[k].substring(2, words[k].length-1);
			saliences[k] = parseFloat(saliences[k].substring(2, saliences[k].length-1));
		} else if (words[k][words.length-1] == "]") {
			words[k] = words[k].substring(1, words[k].length-2);
			saliences[k] = parseFloat(saliences[k].substring(1, saliences[k].length-2));
		} else {
			words[k] = words[k].substring(1, words[k].length-1);
			saliences[k] = parseFloat(saliences[k].substring(1, saliences[k].length-1));
		}
	}
	console.log(words);
	console.log(saliences);

	for (var j = 0; j < words.length; j++) {
		var diam = (saliences[j] * 300+50);
		console.log(words[j], diam);
		function addCircle(){
			for (var y = 100; y < 350; y++) {
				for (var x = 100; x < 350; x++){
					if (doesItFitGrid(grid, diam, x, y) == true) {
						markGrid(grid, diam, x, y);
						circles.push({
							x: x,
							y: y,
							diam: diam,
							word: words[j]
						});
						return
					}
				}
			}
		}
		addCircle();
		console.log(words[j]);
	}
}

function draw() {
	background(255);
	textAlign(CENTER);
	for (var i = 0; i < circles.length; i++) {
		var circle = circles[i];
		fill(43, 88, 118);
		noStroke();
		ellipse(circle.x, circle.y, circle.diam, circle.diam);
		fill(255);
		text(circle.word, circle.x, circle.y);
	}
}
