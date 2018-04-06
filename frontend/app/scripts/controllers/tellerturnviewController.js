'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:tellerturnviewController
 * @description
 * # tellerturnviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('tellerturnviewController',[
    '$scope',
    '$timeout',
    'cardService',
    'timerService',
    function ($scope,$timeout,cardService,timerService) {

    console.log("gp turn view controller.");
    $scope.cardData = cardService.cardData;
    $scope.showCard = true;

    $scope.timer    = timerService.timer;
    $scope.showPlay = false;
    $scope.role     = "Teller";

    $scope.pauseClicked = function(){
      console.log(timerService.timer);
      timerService.timer.pauseTime();
      $scope.showPlay = true;
    };

    $scope.playClicked = function(){
      timerService.timer.resumeTime();
      $scope.showPlay=false;
    };

    $scope.skipCard = function(){
      $scope.showCard = false;

      $timeout(function(){
        cardService.skipCard();
        $scope.showCard = true;
      },400);
    };


}]);
