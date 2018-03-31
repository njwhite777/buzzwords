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
  console.log(gameService.gameServiceData.teams)
  $scope.gameData = {
    maxNumberOfPlayers: 3,
    turnDuration: 30,
    teamNumber: 2,
    turnModifiers: true,
    name:"",
  };

  $scope.gameData.teamData = [];
  $scope.collapseAll = function(data) {
    for (var i in $scope.accordianData){
      if($scope.accordianData[i] != data){
        $scope.accordianData[i].expanded = false;
      };
    }
    data.expanded = !data.expanded;
  };
  // $scope.accordianData = [{'id':10,'name':'workworkwork','teams':['t1','t2','t3']},
  //     {'id':11,'name':'textualChallenge','teams':['red','blue','green']},
  //     {'id':12,'name':'talkTalkTalk','teams':['t1','t2','t3']},
  //     {'id':13,'name':'fearthebeard','teams':['t1','t2','t3']},
  //     {'id':13,'name':'gogogo','teams':['t1','t2','t3']}]

  $scope.accordingData = $scope.gameServiceData.games;
  console.log($scope.accordingData);
//TODO: get game list from socket, not hardcoding.

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
  $scope.joinButton = function(){
    //TODO: add team, game in player;
    $state.go('gameplayerwait');
  }

  $scope.initiateGameButton = function(){
    // TODO: when this happens should send a request to the api that kicks off the game.
    $state.go('gameplayerwait');
  }

  $scope.formFieldChanged = function(){
    gameService.validateGameConfig($scope.gameData);
  }

  $scope.forceBack = function(){
    $scope.isExceed = false;
    if($scope.gameData.maxNumberOfPlayers > 5){
      $scope.gameData.maxNumberOfPlayers = 5;
      console.log("exceed maximun value");
      $scope.isExceed = true;
    }
  }

}]);
