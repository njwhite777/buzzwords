'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:gameplayerturnviewController
 * @description
 * # gameplayerturnviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('gameplayerturnviewController',['$scope','timerService',function ($scope,timerService) {
    console.log(timerService.timer);

    // Note: for the timer widget to work properly, this variable must be attached to the scope.
    $scope.timer = timerService.timer;

    $scope.showPlay= false;

    $scope.pauseClicked = function(){
      console.log(timerService.timer);
      timerService.timer.pauseTime();
      $scope.showPlay=true;
    };

    $scope.playClicked = function(){
      console.log("play");
      timerService.timer.resumeTime();
      $scope.showPlay=false;
    };
    // Emit events on the timer service

}]);
