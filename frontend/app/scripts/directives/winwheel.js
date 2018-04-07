angular.module('frontendApp')
  .directive('winwheel',['timerService','cardService','socketService','$timeout',function(timerService,cardService,socketService,$timeout){
    function link(scope, element, attrs){
      scope.height = "600";
      scope.width  = "600";
      var socket = socketService.gameSocket;
      
      $('#wheelCanvas').attr('width',scope.width);
      $('#wheelCanvas').attr('height',scope.height);

      var theWheel = new Winwheel({
        'canvasId'    : 'wheelCanvas',
        'outerRadius' : ((scope.height/2) - 20),
        'numSegments' : 8,
        'textFontSize' : 18,
        'segments'    :
        [
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#eae56f', 'text' : '2X Turn','size': winwheelPercentToDegrees(2) },
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#fc7ba7', 'text' : '.5 Turn','size': winwheelPercentToDegrees(7)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#7884ea', 'text' : '∞ Skips','size': winwheelPercentToDegrees(7)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#f6a84a', 'text' : 'No Forbidden Words','size': winwheelPercentToDegrees(14)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#89f26e', 'text' : 'Statue Teller','size': winwheelPercentToDegrees(21)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#f6776d', 'text' : 'One Guesser','size': winwheelPercentToDegrees(21)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#BBDEFB', 'text' : 'Round Killer','size': winwheelPercentToDegrees(14)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#b068b1', 'text' : 'All Guess','size': winwheelPercentToDegrees(14)}
        ],
        'lineWidth'   : 0
      });

      var tcanvas = document.getElementById('wheelCanvas');
      var tx = tcanvas.getContext('2d');

      // Ensure that have context before calling function to draw.
      if (tx)
      {
          drawTriangle();
      }
      // Put draw code in a function since would have to call this
      // each frame of the animation to re-draw the pointer.
      function drawTriangle()
      {
          tx.strokeStyle = '#000000';     // Set line colour.
          tx.fillStyle   = '#000000';        // Set fill colour.
          tx.lineWidth   = 0;
          tx.moveTo((scope.width/2)+20, 0);             // Move to initial position.
          tx.beginPath();                 // Begin path.
          tx.lineTo((scope.width/2)-20, 0);             // Draw lines to make the shape.
          tx.lineTo((scope.width/2),100);
          tx.lineTo((scope.width/2)+20, 0);
          tx.stroke();                    // Complete the path by stroking (draw lines).
          tx.fill();                      // Then fill with colour.
      }

      scope.spinWheel = function(){
        var wheel =  {

        };
        socket.emit("roll",wheel);
        console.log("TODO: implement the call to the socket");
        console.log("TODO: Note, currently using gameSocket");
      };

      // TODO:
      var doWheelspinAnimation = function(segmentNumber){
        console.log("TODO: wheelspin animation happened!");
        // var stopAt = theWheel.getRandomForSegment(segmentNumber);
        // theWheel.animation.stopAngle = stopAt;
        // theWheel.startAnimation();
      };
      socket.on('roll_result',doWheelspinAnimation);

    }

    return {
      restrict: 'E',
      link :  link,
      template: '<canvas id=\'wheelCanvas\' >'+
                  'Canvas not supported, use another browser.'+
                '</canvas>',
    };
}]);
