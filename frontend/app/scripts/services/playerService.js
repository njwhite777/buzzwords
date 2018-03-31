'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:playerService
 * @description
 * # playerService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('playerService',['socketService','$http','$q','debug',function(socketService,$http,$q,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.
    if(debug) console.log("player service");

    var socket = socketService.playerSocket;
    var notifySocketReady = socketService.notifySocketReady;
    var socketConnected=false;

    notifySocketReady().then(function(result){socketConnected=true});

    var emitPlayerConnected = function(playerDetails){
      socket.emit('player_login',playerDetails);
    };

    // Causes player credentials to be re-associated with the uuid
    //   when a disconnect, re-connect has happened
    socket.on('disconnect',function(){
      if(debug) console.log("playerService:disconnected from socket");
      socketConnected=false;
      notifySocketReady().then(
        function(result){
          emitPlayerConnected();
        },
        function(result){
          console.log(result);
        }
      );
    });

    var emitPlayerJoined = function(playerDetails){
      if(socketConnected){
        emitPlayerConnected(playerDetails);
      }else{
        notifySocketReady().then(
          function(result){
            socketConnected=true;
            emitPlayerConnected(playerDetails);
          },
          function(result){
            console.log(result);
          }
        );
      }
    }

    return {
      emitPlayerJoined : emitPlayerJoined,
    };

  }]);
