'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:playerService
 * @description
 * # playerService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('playerService',['socketService','$http','loginUser','$q','debug',function(socketService,$http,loginUser,$q,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.
    if(debug) console.log("player service");

    var socket = socketService.playerSocket;
    var notifySocketReady = socketService.notifySocketReady;


    var emitPlayerConnected = function(){
      socket.emit('player_login',loginUser.getPlayerDetails() );
    };

    // Causes player credentials to be re-associated with the uuid
    //   when a disconnect, re-connect has happened
    socket.on('disconnect',function(){
      if(debug) console.log("playerService:disconnected from socket");
      notifySocketReady().then(
        function(result){
          emitPlayerConnected();
        },
        function(result){
          console.log(result);
        }
      );
    });

    return {
      emitPlayerJoined : function(){
        notifySocketReady().then(
          function(result){
            emitPlayerConnected();
          },
          function(result){
            console.log(result);
          }
        );
      }
    };

  }]);
