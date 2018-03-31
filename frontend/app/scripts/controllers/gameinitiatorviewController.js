'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:gameinitialorviewController
 * @description
 * # gameinitiatorviewController
 * Controller of the initial period of game
 */

angular.module('frontendApp')
      .controller('gameinitiatorviewController',['$scope',function($scope){
        console.log("GameIV Controller");

  $scope.gameStateValid = function(){
    return true;
  };

}]);
