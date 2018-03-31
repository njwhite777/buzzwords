'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:tellerturnviewController
 * @description
 * # tellerturnviewController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('tellerturnviewController',['$scope',function ($scope) {

    console.log("gp turn view controller.");
    $scope.card = {
      buzzword : 'alphabet',
      forbiddenwords : ['a','b','c','d']
    };

    $scope.skipCard = function(){

    };


}]);
