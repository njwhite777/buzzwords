'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:tellerturnviewController
 * @description
 * # tellerturnviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('tellerturnviewController',[
    '$scope',
    '$timeout',
    'timerService',
    function ($scope,$timeout,timerService) {

    $scope.timer    = timerService.timer;
    $scope.showPlay = false;
    $scope.role     = "Teller";

    $scope.it = {
      size : 36,
    };


}]);
