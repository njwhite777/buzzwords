'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:gameinitialorviewController
 * @description
 * # gameinitiatorviewController
 * Controller of the initial period of game
 */

angular.module('frontendApp')
      .controller('gameinitiatorviewController',[
        '$scope',
        'viewSwapService',
        'gameService',
        function($scope,viewSwapService,gameService) {
          $scope.gameService = gameService;
          $scope.switchedElements = viewSwapService.switchedElements;
        }
      ]);
