angular.module('frontendApp')
  .directive('countdown',['timerService',function(timerService){

    function link(scope, element, attrs){
      var canvas = angular.element(document.querySelector('#canvas'))[0];
      var ctx = canvas.getContext('2d');
      var start = null;

      var timerColor = attrs.timercolor;
      var centerColor = attrs.centercolor;
      var textColor = attrs.textColor;

      // Set up $scope.timer in controller.
      var timer = scope.timer;

      if(!attrs.timercolor) timerColor = 'rgb(30, 136, 229)';
      if(!attrs.centercolor) centerColor = '#263238';
      if(!attrs.textcolor) textColor = '#ffffff';

      if(scope.timer.dimensions && scope.timer.dimensions.height){
        canvas.width = scope.timer.dimensions.height;
        canvas.height = scope.timer.dimensions.height;
      }else if(attrs.height && attrs.width){
        canvas.height = attrs.height;
        canvas.width = attrs.width;
      }else{
        canvas.width = 200;
        canvas.height = 200;
      }

      var cHelper = {};
      cHelper.centerCircle = function(){
          return canvas.height/4;
      };
      cHelper.outerCircle = function(){
          return canvas.height/4;
      };
      cHelper.thickness = function(){
        return canvas.height/3.5;
      },
      cHelper.centerCircleThickness = function(){
        return canvas.height/4;
      };
      cHelper.centerX= function(){
        return canvas.width/2;
      },
      cHelper.centerY= function(){
        return canvas.height/2;
      }
      cHelper.fontSize = '24px';
      cHelper.zeroStart = 0;
      cHelper.fullCircle = 2 * Math.PI;
      cHelper.start = (3 * Math.PI) / 2;

      function init()
      {
        window.requestAnimationFrame(draw);
      }

      function draw(now)
      {
        // Give the start time its initial value.
        if(!start)start = now;
        // This will be zero the first time it is called.
        var progress = now - start;
        var transpired = timer.transpired;
        var duration =  timer.duration;
        // Use the milliseconds to calculate the distance in degrees.
        function degCalc(duration,transpired){
          return (360*(transpired*1000))/(duration*1000);
        };

        function rad(deg){
          return  (Math.PI / 180) * deg;
        }

        var displayRemainSec = duration - transpired;
        var displayRemainMins = Math.floor( displayRemainSec / 60 );

        drawRect(0, 0, canvas.width, canvas.height, '#FAFAFA');
        // x, y, radius, start, end, clockwise, color, type, thickness
        if(timer.status=='running'){
          drawCircle(cHelper.centerX(), cHelper.centerY(), cHelper.outerCircle(), cHelper.start, rad(degCalc(duration,transpired)) + cHelper.start, false, timerColor, 'stroke', cHelper.thickness()); //hour
        }
        if(timer.status == 'initializing'){
          drawCircle(cHelper.centerX(), cHelper.centerY(), cHelper.outerCircle(), cHelper.start, rad(360) + cHelper.start, false, timerColor, 'stroke', cHelper.thickness()); //hour
        }
        drawCircle(cHelper.centerX(), cHelper.centerY(), cHelper.centerCircle(), cHelper.zeroStart, cHelper.fullCircle, false, centerColor, 'fill', cHelper.centerCircleThickness); //inner

        if(timer.status=='running'){
          drawText(`${displayRemainMins.toString().length == 1?'0'+displayRemainMins:displayRemainMins}:${displayRemainSec.toString().length == 1?'0'+displayRemainSec:displayRemainSec}`, canvas.width / 2 - 42, canvas.height / 2 + 15, textColor, cHelper.fontSize);
        }
        if(timer.status=='initializing'){
          drawText(`00:00`, canvas.width / 2 - 36, canvas.height / 2 + 10, textColor, cHelper.fontSize);
        }
        if(progress < 975){
          window.requestAnimationFrame(draw);
        }
      }

      function drawText(text, x, y, color, size, font) {
        if(!font) font = "Cabin";
        ctx.font = `${size} ${font}`;
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
      // Kicks things off.
      init();
    }

    return {
      restrict: 'E',
      link : link,
      template: '<canvas id="canvas"></canvas>',
    };
}]);
