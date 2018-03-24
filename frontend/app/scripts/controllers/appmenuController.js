'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:appmenuController
 * @description
 * # menuController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('appmenuController', [
    '$scope',
    'gameService',
    function ($scope,gameService) {

      $scope.games  = gameService.games;

  }]);
