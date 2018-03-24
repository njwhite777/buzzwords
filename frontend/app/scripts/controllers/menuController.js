'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:menuController
 * @description
 * # menuController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('menuController', [
    '$scope',
    'gameService',
    function ($scope,gameService) {

      $scope.games  = gameService.games;

  }]);
