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
      '$state',
      'timerService',
      'debug',
      function ($scope,$state,timerService,debug) {
        if(debug)  console.log("moderator View Controller");

        $scope.timer = timerService.timer;
        $scope.showPlay= false;
        $scope.role     = "Moderator";

        //change points for one team
        $scope.addPoints = function(team){
          //TODO: function to put points to team
        }
        $scope.minusPoints = function(team){
          //TODO: function to minus points to team
        }

        $scope.pauseClicked = function(){
          console.log(timerService.timer);
          timerService.timer.pauseTime();
          $scope.showPlay=true;
        };
        $scope.playClicked = function(){
          console.log("play");
          timerService.timer.resumeTime();
          $scope.showPlay=false;
        };



  // Do things in the drawer view.

}]);
