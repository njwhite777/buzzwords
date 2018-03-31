'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:gameplayerturnviewController
 * @description
 * # gameplayerturnviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('gameplayerturnviewController',['$scope',function ($scope) {

    $scope.secondsRemaining = 30;
    $scope.gameData = {

    };
    // $scope.gameData.team
    // gameData.teller
    // gameData.moderator
    // gameData.modifier

}]);
