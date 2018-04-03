'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:playerService
 * @description
 * # playerService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('playerService',['socketService','$http','$q','loginUser','debug',function(socketService,$http,$q,loginUser,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.
    if(debug) console.log("player service");

    var socket = socketService.playerSocket;
    var notifySocketReady = socketService.notifySocketReady;
    var notifyPlayerReady = loginUser.waitForPlayerDetails;

    var emitPlayerConnected = function(playerDetails){
      socket.emit('player_login',playerDetails);
    };

    // Causes player credentials to be re-associated with the uuid
    //   when a disconnect, re-connect has happened
    socket.on('disconnect',function(){
      // TODO: figure out stuff here.
      $q.all([notifySocketReady()]).then(
        function(result){
          console.log(loginUser.getPlayerDetails());
          emitPlayerConnected(loginUser.getPlayerDetails());
        },
        function(result){
          console.log(result);
        }
      );
    });
    var emitPlayerJoined = function(){
        $q.all([notifyPlayerReady(),notifySocketReady()]).then(
          function(result){
            console.log(loginUser.getPlayerDetails());
            emitPlayerConnected(loginUser.getPlayerDetails());
          },
          function(result){
            console.log(result);
          }
        );
    }
    emitPlayerJoined();
  }]);
