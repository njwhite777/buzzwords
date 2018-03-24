'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:gamemenuviewController
 * @description
 * # gamemenuviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('gamemenuviewController', function ($scope) {

    $scope.name = "hanqing",
    $scope.teamNumber = 0


  console.log("here is gamemenuviewController!");
  console.log("teamNumber is " + $scope.teamNumber)

});
