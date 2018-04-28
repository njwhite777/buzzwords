angular.module('frontendApp')
  .directive('winwheel',[
    'timerService',
    'cardService',
    'socketService',
    '$timeout',
    function(timerService,cardService,socketService,$timeout){


      function link(scope, element, attrs){

        scope.height = "400";
        scope.width  = "400";
        scope.duration = 4;
        scope.turns = 4;
        scope.segments = [
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#eae56f', 'text' : '2X Turn','size': winwheelPercentToDegrees(2) },
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#fc7ba7', 'text' : '.5X Turn','size': winwheelPercentToDegrees(7)},
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#7884ea', 'text' : '∞ Skips','size': winwheelPercentToDegrees(7)},
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#f6a84a', 'text' : 'No Forbidden Words','size': winwheelPercentToDegrees(14)},
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#89f26e', 'text' : 'Statue Teller','size': winwheelPercentToDegrees(15)},
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#f6776d', 'text' : 'One Guesser','size': winwheelPercentToDegrees(15)},
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#BBDEFB', 'text' : 'Turn Killer','size': winwheelPercentToDegrees(14)},
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#b068b1', 'text' : 'All Guessers','size': winwheelPercentToDegrees(14)},
          {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#4068bb', 'text' : 'Normal Turn','size': winwheelPercentToDegrees(12)}
        ];
        scope.numSegments = scope.segments.length;

        var socket = socketService.gameSocket;

        $('#pointerOverlay').attr('width',scope.width);
        $('#pointerOverlay').attr('height',scope.height);
        $('#wheelCanvas').attr('width',scope.width);
        $('#wheelCanvas').attr('height',scope.height);

        // Ensure that have context before calling function to draw.
        // Put draw code in a function since would have to call this
        // each frame of the animation to re-draw the pointer.
        scope.myWheel = new Winwheel({
          'canvasId'    : 'wheelCanvas',
          'outerRadius' : ((scope.height/2) - 20),
          'numSegments' : scope.numSegments,
          'textFontSize' : 18,
          'segments'    : scope.segments,
          'lineWidth'   : 0,
          'animation' :
          {
              'type'          : 'spinToStop',
              'duration'      : scope.duration,
              'spins'         : scope.turns
          }
        });


        scope.drawTriangle = function(){
            var pointerOverlay = document.getElementById('pointerOverlay');
            var ctx = pointerOverlay.getContext('2d');
            ctx.fillStyle = "rgba(255,255,255, 0)";
            ctx.fillRect(0, 0, scope.width, scope.height);
            ctx.strokeStyle = '#000000';     // Set line colour.
            ctx.fillStyle   = '#000000';        // Set fill colour.
            ctx.lineWidth   = 0;
            ctx.moveTo((scope.width/2)+10, 0);             // Move to initial position.
            ctx.beginPath();                 // Begin path.
            ctx.lineTo((scope.width/2)-10, 0);             // Draw lines to make the shape.
            ctx.lineTo((scope.width/2),70);
            ctx.lineTo((scope.width/2)+10, 0);
            ctx.stroke();                    // Complete the path by stroking (draw lines).
            ctx.fill();                      // Then fill with colour.
        };

        scope.drawTriangle();

        scope.spinWheel = function(){
          var wheel =  {
            gameID : scope.game.id,
            duration : scope.duration
          };
          socket.emit("roll_wheel",wheel);
        };

        socket.on('my_roll_result',function(data){
          segmentNumber = data['rollID']+1;
          var stopAt = scope.myWheel.getRandomForSegment(segmentNumber);
          scope.myWheel.animation.stopAngle = stopAt;
          scope.myWheel.startAnimation();
          $timeout(function(){
            Object.assign(scope.turn.modifier,data);
          }, scope.duration*1000 );
        });

        socket.on('enable_start_turn_button',function(){
            scope.disabledStart = false;
        });

      }

      return {
        restrict: 'E',
        link :  link,
        template: '<canvas id=\'pointerOverlay\' style="position:absolute;">'+
                  '</canvas>'+
                  '<canvas id=\'wheelCanvas\' >'+
                  'Canvas not supported, use another browser.'+
                  '</canvas>'
      };
}]);
