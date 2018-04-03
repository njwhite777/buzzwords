'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:appmenuController
 * @description
 * # menuController
 * Controller of the left drawer of the application
 */
angular.module('frontendApp')
  .controller('appmenuController', [
    '$scope',
    'loginUser',
    '$window',
    function ($scope,loginUser,$window) {
      $scope.loginUser = loginUser;

      $scope.userLogOut = function(){
        loginUser.deleteEmail();
        $window.location.reload();
      };

  }]);
