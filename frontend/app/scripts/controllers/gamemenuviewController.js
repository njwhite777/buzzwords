'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:gamemenuviewController
 * @description
 * # gamemenuviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('gamemenuviewController', ['$scope','gameService',function ($scope,gameService) {

    $scope.teamData = {
      teamNumber : 0,
      team : [],
    };

  $scope.games = gameService.games;

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

}]);
