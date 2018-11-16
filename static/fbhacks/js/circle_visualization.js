var data = {
	"Boston": .3,
	"technology": .8,
	"Kristin": .2,
	"swimming": .1,
	"swimming": .9
};

var circles = [];

function setup() {
	var width = 400;
	var height = 400;
	var canvas = createCanvas(width, height);
	noLoop();
	canvas.parent('p5-canvas');
	for (var key in data) {
		console.log(data[key]);
		var diam = (data[key]) * 60 +20;
		var fits = false;
		while (!fits) {
			var x = Math.random() * (width-3/2*diam) + diam/2;
			var y = Math.random() * (height-3/2*diam) + diam/2;
			var no_conflicts = true;
			for (var i = 0; i < circles.length; i++) {
				var circle = circles[i];
				var dist_between = Math.sqrt(Math.pow(circle.x-x, 2) + Math.pow(circle.y-y, 2));
				if (dist_between < diam/2.0 + circle.diam/2.0) {
					no_conflicts = false;
				}
			}
			if (no_conflicts) {
				circles.push({
					x: x,
					y: y,
					diam: diam,
					word: key
				});
				fits = true;
			}
		}
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