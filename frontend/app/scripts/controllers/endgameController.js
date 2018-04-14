'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:endgameController
 * @description
 * # endgameController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('endgameController',[
    '$scope',
    '$state',
    function ($scope,$state) {

      $scope.finishedGame = function(){
          // TODO: notify that player is no longer in a game.
          console.log("FINISHED GAME!");
          $state.go('root');
      };

    }
]);
