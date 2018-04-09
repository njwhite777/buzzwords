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
        'currentGameService',
        function($scope,viewSwapService,gameService,currentGameService) {
          $scope.currentGameService = currentGameService;
          $scope.switchedElements = viewSwapService.switchedElements;
        }
      ]);
