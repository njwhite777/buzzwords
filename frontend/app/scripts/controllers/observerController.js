'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:observerController
 * @description
 * # observerController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('observerController',['$scope','timerService','gameService','currentGameService',function ($scope,timerService,gameService,currentGameService) {
    $scope.timer = timerService.timer;
    $scope.showPlay= false;
    $scope.role    = "Observer";
    $scope.game = currentGameService.currentGame;
    $scope.turn = currentGameService.currentTurn;
}]);
