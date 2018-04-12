'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:guesserController
 * @description
 * # guesserController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('guesserController',['$scope','timerService','gameService','currentGameService',function ($scope,timerService,gameService,currentGameService) {
    console.log(timerService.timer);
    // Note: for the timer widget to work properly, this variable must be attached to the scope.
    $scope.showPlay= false;
    $scope.role    = "Guesser";
    $scope.game = currentGameService.currentGame;
    $scope.turn = currentGameService.currentTurn;
}]);
