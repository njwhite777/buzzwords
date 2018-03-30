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
  $scope.gameServiceData = gameService.gameServiceData;
  $scope.gameData = {
    maxNumberOfPlayers: 3,
    turnDuration: 30,
    teamNumber: 2,
    turnModifiers: true,
    name:"",
  };

  $scope.gameData.teamData = [];

  $scope.$watch('gameData.teamNumber', function (newVal,oldVal) {
    console.log(newVal);
    $scope.gameData.teamData = (
      function(){
          var teams=[];
          for(var i=0;i<newVal;i++){
            teams.push({"name" : "team"+(i+1),"prettyName" : "Team " +(i+1) });
          }
          return teams;
        })();
  });

  $scope.initiateGameButton = function(){
    // TODO: when this happens should send a request to the api that kicks off the game.
    $state.go('gameplayerwait');
  }

  $scope.formFieldChanged = function(){
    gameService.validateGameConfig($scope.gameData);
  };

}]);
