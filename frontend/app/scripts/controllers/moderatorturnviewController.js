'use strict';

/**
 * @ngdoc function
<<<<<<< HEAD
 * @name frontendApp.controller:gameinitialorviewController
 * @description
 * # gameinitiatorviewController
 * Controller of the initial period of game
 */
 angular.module('frontendApp')
  .controller('moderatorturnviewController', [
      '$scope',
      'viewSwapService',
      '$state',
      'debug',
      function ($scope,viewSwapService,$state,debug) {
        if(debug)  console.log("moderator View Controller");
        $scope.data = viewSwapService.data

        //change points for one team
        $scope.addPoints = function(team){
          //TODO: function to put points to team
        }
        $scope.minusPoints = function(team){
          //TODO: function to minus points to team
        }



  // Do things in the drawer view.

}]);
