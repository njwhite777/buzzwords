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
    // Note: for the timer widget to work properly, this variable must be attached to the scope.
    $scope.showPlay= false;
    $scope.role    = "Observer";

}]);
