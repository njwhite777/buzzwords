'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:gamemenuviewController
 * @description
 * # gamemenuviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('gamemenuviewController', [
    '$scope',
    'gameService',
    '$state',
    '$http',
    'debug',
function ($scope,gameService,$state,$http,debug) {

  if(debug) console.log("GM View controller");
  // Note: The games service is responsible for keeping the gameData object up to date.
  //  as long as we are using an object e.g. "{}" changes are automatically detected and synchronzied!
  $scope.gameData = gameService.gameData;
  $scope.teamData = {
    teamNumber : 0,
    team : [],
  };

  $scope.$watch('teamData.teamNumber', function (newVal,oldVal) {
    $scope.teamData.team = (
      function(){
          var teams=[];
          for(var i=0;i<newVal;i++){
            teams.push("team"+i)
          }
          return teams;
        })();
  });

  $scope.initiateGameButton = function(){
    // TODO: when this happens should send a request to the api that kicks off the game.
    $state.go('gameplayerwait');
  }

  $scope.teamFieldChanged = function(){
    // TODO: once this gets called, should send a request off to the api to verify if the game state is valid.
    //  if the game state is valid, should enable the submit button.
    console.log($scope.createGameForm);
  };

}]);
