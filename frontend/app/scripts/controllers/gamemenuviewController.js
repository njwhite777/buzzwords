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
    'loginUser',
    'debug',
function ($scope,gameService,$state,$http,loginUser,debug) {

  if(debug) console.log("GM View controller");

  // Note: The games service is responsible for keeping the gameData object up to date.
  //  as long as we are using an object e.g. "{}" changes are automatically detected and synchronzied!
  $scope.gameServiceData = gameService.gameServiceData;
  console.log(gameService.gameServiceData.teams)
  $scope.gameData = {
    maxPlayersPerTeam: 3,
    turnDuration : 30,
    pointsToWin : 30,
    numberOfTeams: 2,
    skipPenaltyAfter : 3,
    gameChangers : true,
    name:""
  };
  $scope.turnDurationOptions= [20,30,60];
  $scope.skipOptions= ['infinite',0,3,5];

  $scope.gameData.teamData = [];
  $scope.collapseAll = function(data) {
    for (var i in $scope.accordianData){
      if($scope.accordianData[i] != data){
        $scope.accordianData[i].expanded = false;
      };
    }
    data.expanded = !data.expanded;
  };

  $scope.accordingData = $scope.gameServiceData.games;
  console.log($scope.accordingData);
//TODO: get game list from socket, not hardcoding.

  $scope.$watch('gameData.numberOfTeams', function (newVal,oldVal) {
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
  $scope.joinButton = function(game,team){
    //TODO: add team, game in player;
    var player = loginUser.getPlayerDetails();
    var data = {'gameID':game.id,'teamID': team.id,'player':player.email};
    gameService.playerJoinTeam(data);
  }

  $scope.initiateGameButton = function(){
    gameService.initGame();
  }

  $scope.formFieldChanged = function(field){
    if(field!="" || field != undefined) gameService.validateGameConfig($scope.gameData);
  }

  $scope.forceBack = function(object,fieldString,max,min){

    if(object[fieldString] > max){
      alert(fieldString + " cannot larger than" + max);
      object[fieldString] = max;
    }else if(object < min){
      object[fieldString] = min;
      alert(fieldString + " cannot less than" + min);
    }
  }

  $scope.getData = function(){
    if(debug){
      console.log($scope.gameData.selectedFreeSkips);
    };
  };

}]);
