'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:viewSwapService
 * @description
 * # viewSwapService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('viewSwapService',['socketService','$state','debug',function(socketService,$state,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.
    var socket = socketService.viewSocket;



  }]);
