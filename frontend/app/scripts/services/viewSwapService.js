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

    socket.on('swap_view',function(message){
      if(debug) console.log("viewswapservice:swap_view");
      if(debug) console.log(message);

      if(message['turn_view'] == 'moderatorturn'){
        data = message['data'];
        $state.go('moderatorturn');
      }
      if(message['turn_view'] == 'tellerrolldie'){
        data = message['data'];
        $state.go('tellerrolldie')
      }
      if(message['turn_view'] == 'tellerturn' ){
        data = message['data'];
        $state.go('tellerturn');
      }
      if(message['turn_view'] == 'gameplayerturn'){
        data = message['data'];
        $state.go('gameplayerturn');
      }
    });

    return {
      data : data
    };

  }]);
