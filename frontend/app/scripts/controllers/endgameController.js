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
    'pointsService',
    function ($scope,$state,pointsService) {
      $scope.teamScoreData = pointsService.teamScoreData;
      $scope.finishedGame = function(){
          $state.go('root');
      };
    }
]);
