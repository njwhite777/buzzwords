'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:guesserController
 * @description
 * # guesserController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('guesserController',['$scope','timerService','gameService',function ($scope,timerService,gameService) {
    console.log(timerService.timer);
    // Note: for the timer widget to work properly, this variable must be attached to the scope.
    $scope.timer = timerService.timer;
    $scope.showPlay= false;
    $scope.role    = "Guesser";
    $scope.gameService=gameService;

}]);
