angular.module('frontendApp')
  .directive('winwheel',['timerService','cardService','$timeout',function(timerService,cardService,$timeout){



    function link(scope, element, attrs){
      scope.height = "600";
      scope.width  = "600";
      $('#wheelCanvas').attr('width',scope.width);
      $('#wheelCanvas').attr('height',scope.height);
      var theWheel = new Winwheel({
        'canvasId'    : 'wheelCanvas',
        'outerRadius' : ((scope.height/2) - 20),
        'numSegments' : 8,
        'textFontSize' : 16,
        'segments'    :
        [
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#eae56f', 'text' : '2X Turn','size': winwheelPercentToDegrees(2) },
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#7884ea', 'text' : '.5 Turn','size': winwheelPercentToDegrees(7)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#fc7ba7', 'text' : '∞ Skips','size': winwheelPercentToDegrees(7)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#BBDEFB', 'text' : 'No Forbidden Words','size': winwheelPercentToDegrees(14)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#89f26e', 'text' : 'Statue Teller','size': winwheelPercentToDegrees(21)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#f6776d', 'text' : 'One Guesser','size': winwheelPercentToDegrees(21)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#BBDEFB', 'text' : 'Round Killer','size': winwheelPercentToDegrees(14)},
            {'textFontFamily' : 'Cabin','strokeStyle': 'rgba(255,255,255,0)','fillStyle' : '#fe5409', 'text' : 'All Guess','size': winwheelPercentToDegrees(14)}
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
        tx.moveTo((scope.width/2)+10, 0);             // Move to initial position.
        tx.beginPath();                 // Begin path.
        tx.lineTo((scope.width/2)-10, 0);             // Draw lines to make the shape.
        tx.lineTo((scope.width/2),100);
        tx.lineTo((scope.width/2)+10, 0);
        tx.stroke();                    // Complete the path by stroking (draw lines).
        tx.fill();                      // Then fill with colour.
    }


    console.log(theWheel.segments)
    }

    return {
      restrict: 'E',
      link :  link,
      template: '<canvas id=\'wheelCanvas\' >'+
                  'Canvas not supported, use another browser.'+
                '</canvas>',
    };
}]);
