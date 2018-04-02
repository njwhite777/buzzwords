'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:gameinitialorviewController
 * @description
 * # gameinitiatorviewController
 * Controller of the initial period of game
 */

angular.module('frontendApp')
      .controller('gameinitiatorviewController',['$scope','viewSwapService',function($scope,viewSwapService){
        console.log("GameIV Controller");
        $scope.switchedElements = viewSwapService.switchedElements;
        
}]);
