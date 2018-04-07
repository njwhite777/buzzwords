'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:observerController
 * @description
 * # observerController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('observerController',['$scope','timerService','gameService',function ($scope,timerService,gameService) {
    // Note: for the timer widget to work properly, this variable must be attached to the scope.
    $scope.timer = timerService.timer;
    $scope.showPlay= false;
    $scope.role    = "Observer";
    $scope.gameService = gameService;
}]);
