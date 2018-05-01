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
    '$mdToast',
    '$rootScope',
    'debug',
function ($scope,gameService,$state,$http,loginUser,$mdToast,$rootScope,debug) {

  if(debug) console.log("GM View controller");

  // Note: The games service is responsible for keeping the gameData object up to date.
  //  as long as we are using an object e.g. "{}" changes are automatically detected and synchronzied!
  $scope.games = gameService.games;

  $scope.gameCreateData = gameService.gameCreateData;

  $scope.gameData = {
    maxPlayersPerTeam: 3,
    turnDuration : 60,
    pointsToWin : 30,
    numberOfTeams: 2,
    skipPenaltyAfter : 3,
    maxRoundsPerGame: 5,
    gameChangers : true,
    name:""
  };

  $scope.turnDurationOptions= [30,60,90,120];
  $scope.skipOptions= ['infinite',0,3,5];
  $scope.pointsOptions= [10,30,60];
  $scope.prettyOptions={
    'skipPenaltyAfter' : 'Free Skips',
    'maxPlayersPerTeam': 'Max Players/Team',
    'numberOfTeams' : 'Number of Teams',
    'pointsToWin' : 'Points to Win',
    'maxRoundsPerGame': "The maximum rounds per game"
  }

  $scope.gameData.teamData = [];
  $scope.collapseAll = function(data) {
    for (var i in $scope.accordianData){
      if($scope.accordianData[i] != data){
        $scope.accordianData[i].expanded = false;
      };
    }
    data.expanded = !data.expanded;
  };


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
    console.log("Player Joining Team: ",game,team);
    var data = {'gameID':game.id,'teamID': team.id,'player':player.email};
    gameService.playerJoinTeam(data);
  }

  $scope.initiateGameButton = function(){
    gameService.initGame();
  }

  $scope.formFieldChanged = function(data){
    gameService.validateGameConfig(data);
  }

  $scope.forceBack = function(object,fieldString,max,min){

    if(object[fieldString] > max){
      object[fieldString] = max;
      $scope.showSimpleToast($scope.prettyOptions[fieldString] + " cannot be larger than " + max);
    }else if(object[fieldString] < min){
      object[fieldString] = min;
      $scope.showSimpleToast($scope.prettyOptions[fieldString] + " cannot be less than " + min);
    }
  }

  $scope.toastPosition = {
    bottom: true,
    right: true
  };

  $scope.getToastPosition = function() {

    return Object.keys($scope.toastPosition)
      .filter(function(pos) { return $scope.toastPosition[pos]; })
      .join(' ');
  };

  $scope.showSimpleToast = function(text) {
    var pinTo = $scope.getToastPosition();
    console.log($mdToast.simple());
    $mdToast.show(
      $mdToast.simple()
        .textContent(text)
        .position(pinTo )
        .hideDelay(3000)
    );
  };

  $rootScope.$on('invalid_game_message',function(event,data){
    console.log(data);
    $scope.showSimpleToast(data.message);
  });

}]);
