'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:tellerturnviewController
 * @description
 * # tellerturnviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('turnwaitviewController',[
    '$scope',
    'pointsService',
    function ($scope,pointsService) {
      $scope.teamScoreData = pointsService.teamScoreData;
    }
]);
