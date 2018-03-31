'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:viewSwapService
 * @description
 * # viewSwapService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('viewSwapService',[
    'socketService',
    '$state',
    'debug',
    function(socketService,$state,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.
    var socket = socketService.viewSocket;
    var data = {};

    socket.on('swap_view',function(data){
      if(debug) console.log("viewswapservice:swap_view");
      if(debug) console.log(data);
      console.log($state);
      $state.go(data['swapView']);
    });

    return {
      data : data
    };

  }]);
