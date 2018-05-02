app.directive('buzzer',['$interval',function ($interval) {

  function link(scope, element, attrs) {

      var promise;
      var audio = new Audio('sounds/buzzer.mp3');

      scope.mouseDown = function() {
        audio.currentTime = 0;
        audio.play();

        var repeat = ((audio.duration*1000) - 10);
        console.log(repeat)

        promise = $interval(function () {
          audio.currentTime = 0;
          audio.play();
        }, repeat);
      };

      scope.mouseUp = function () {
        $interval(function(){
          $interval.cancel(promise);
          promise = null;
        },200);
      };
    }

   return {

      template: '<md-button layout-padding class="md-warn" >'+
                  '<md-icon  ng-style=\"{\'font-size\': it.size + \'px\', height: it.size + \'px\',width:it.size+\'px\'}\" >notifications_active</md-icon>'+
                '</md-button>',
      restrict: 'E',
      link: link
  };
}]);
