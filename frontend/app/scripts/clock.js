
function draw(now)
{
	var centerX = canvas.width / 2,
		centerY = canvas.height / 2,
	var sec = 30;
	var radH = 360*29/30;
	drawRect(0, 0, canvas.width, canvas.height, '#202833');
	drawCircle(centerX, centerY, 110, threePIByTwo, rad(radH) + threePIByTwo, false, '#27AE61', 'stroke', 90); //hour
	drawCircle(centerX, centerY, 95, 0, Math.PI * 2, false, '#263238', 'fill', '50'); //inner
	drawText(`${min.toString().length == 1?'0'+min:min}:${sec.toString().length == 1?'0'+sec:sec}`, canvas.width / 2 - 63, canvas.height / 2 + 15, '#ffffff', '40px');
	drawText(amOrPm, canvas.width / 2 - 15, canvas.height / 2 + 50, '#ffffff', '25px');
	window.requestAnimationFrame(draw);
}

init();

function rad(deg){
	return  (Math.PI / 180) * deg;
}

function drawText(text, x, y, color, size) {
	ctx.font = `${size} "Passion One"`;
	ctx.fillStyle = color;
	ctx.fillText(text, x, y);
}

function drawRect(x, y, width, height, color) {
	ctx.fillStyle = color;
	ctx.fillRect(x, y, width, height);
}

function drawArc(x, y, radius, start, end, clockwise)
{
	ctx.beginPath();
	ctx.arc(x, y, radius, start, end, clockwise);
}

function drawCircle(x, y, radius, start, end, clockwise, color, type, thickness) {
	if(type == 'fill')
	{
		ctx.fillStyle = color;
		drawArc(x, y, radius, start, end, clockwise)
		ctx.fill();
	}
	else if(type == 'stroke')
	{
		ctx.strokeStyle = color;
		ctx.lineWidth = thickness;
		drawArc(x, y, radius, start, end, clockwise)
		ctx.stroke();
	}
}
