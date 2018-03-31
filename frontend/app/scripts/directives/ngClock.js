
angular.module('frontendApp').directive('ngClock', function($timeout) {
  var ctrl = function($scope, $element, $attributes) {
    var numberFills = {
      0: [0,1,2,3,5,6],
      1: [2,6],
      2: [1,2,3,4,5],
      3: [1,2,3,6,5],
      4: [0,3,2,6],
      5: [1,0,3,6,5],
      6: [1,0,3,4,5,6],
      7: [1,2,6],
      8: [0,1,2,3,4,5,6],
      9: [0,1,2,3,6]
    };

    function createDigits() {
      $scope.digit = [];
      for (var i = 0; i < 7; i++) {
        $scope.digit.push('');
      }
      $timeout(function(){
        getTime();
      },300);
    }

    function updatePair(pair, number){
      var number1 = 0;
      var number2 = number;
      var cells = [];
      var cell = [];
      var i = 0;
      var cellareas = angular.element($element).children();
      if (number > 9) {
        //split into two
        number1=number[0];
        number2=number[1];
      }
      if (number1 > -1) {
        cells = angular.element(cellareas[pair]).children();
        for (i = 0; i < cells.length; i++) {
          cell = angular.element(cells[i]);
          if(numberFills[number1].indexOf(i) >= 0) {
            cell.css({
              'opacity': '1'
            });
          } else {
            cell.css({
              'opacity': '0'
            });
          }
        }
      }
      if (number2 > -1) {
        cells = angular.element(cellareas[pair+1]).children();
        for (i = 0; i < cells.length; i++) {
          cell = angular.element(cells[i]);
          if(numberFills[number2].indexOf(i) >= 0) {
            cell.css({
              'opacity': '1'
            });
          } else {
            cell.css({
              'opacity': '0'
            });
          }
        }
      }

    }

    function getTime() {
      var d=new Date();
      var h=d.getHours();
      var m=d.getMinutes();
      var s=d.getSeconds();

      $scope.hour = h;
      $scope.minute = m;
      $scope.second = s;

      $timeout(function(){
        getTime();
      },1000);
    }


    $attributes.$observe('hour', function(value){
      updatePair(0, value);
    });
    $attributes.$observe('minute', function(value){
      updatePair(2, value);
    });
    $attributes.$observe('second', function(value){
      updatePair(4, value);
    });
    createDigits(); // Calls gettime


  };
  return {
    restrict: 'EA',
    replace: true,
    transclude: true,
    scope: true,
    link: ctrl,
    template: '<div ng-transclude></div>'
  };

});
