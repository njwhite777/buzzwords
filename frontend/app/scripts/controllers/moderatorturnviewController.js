'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:moderatorturnviewController
 * @description
 * # moderatorturnviewController
 *
 */
 angular.module('frontendApp')
  .controller('moderatorController', [
      '$scope',
      '$state',
      '$mdToast',
      'debug',
      function ($scope,$state,$mdToast,debug) {
        if(debug)  console.log("moderator View Controller");

        $scope.it = {
          size : 36,
        };

        $scope.role  = "Moderator";

        $scope.showSimpleToast = function() {
          var pinTo = $scope.getToastPosition();
          $mdToast.show(
            $mdToast.simple()
              .textContent('Simple Toast!')
              .position(pinTo )
              .hideDelay(3000)
            );
        };

        $scope.buzz = function(){
          // TODO
          var audio = document.getElementById("buzzer");
          audio.play();
          console.log("TODO: implement audio buzz.");
        };
}]);
