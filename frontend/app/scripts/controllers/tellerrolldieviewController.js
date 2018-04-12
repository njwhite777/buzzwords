'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:tellerrolldieviewController
 * @description
 * # tellerrolldieviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('tellerrolldieviewController',['$scope','gameService','currentGameService',function ($scope,gameService,currentGameService) {
    $scope.game = currentGameService.currentGame;
    $scope.turn = currentGameService.currentTurn;
    $scope.currentGameService = currentGameService;
    $scope.rollButton = true;
    $scope.disabledStart = true;
}]);
