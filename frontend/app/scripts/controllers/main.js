'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('MainCtrl', [
    '$scope',
    'deepstreamService',
    '$state',
    '$timeout',
    '$mdSidenav',
    '$log',
  function ($scope,ds,$state,$timeout,$mdSidenav,$log) {

    function debounce(func, wait, context) {
      var timer;
      return function debounced() {
        var context = $scope, args = Array.prototype.slice.call(arguments);
        $timeout.cancel(timer);
        timer = $timeout(function() {
          timer = undefined;
          func.apply(context, args);
        }, wait || 10);
      };
    }

    function buildDelayedToggler(navID) {
      return debounce(function() {
        // Component lookup should always be available since we are not using `ng-if`
        $mdSidenav(navID)
          .toggle()
          .then(function () {
            $log.debug("toggle " + navID + " is done");
          });
      }, 200);
    }

    // function buildToggler(navID) {
    //   return function() {
    //     // Component lookup should always be available since we are not using `ng-if`
    //     $mdSidenav(navID)
    //       .toggle()
    //       .then(function () {
    //         $log.debug("toggle " + navID + " is done");
    //       });
    //   };
    // }

    $scope.toggleLeftDrawer = buildDelayedToggler('left');

  }]);
