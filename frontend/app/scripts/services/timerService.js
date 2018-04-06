'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:timerService
 * @description
 * # timerService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('timerService',[
    'socketService',
    'gameService',
    '$state',
    'debug',
    function(socketService,gameService,$state,debug){

      console.log("in timerService");
    // Timer is an object so that it can be utilized by our front end to update if need be.
    var timer = {
      status : "initializing",
    };

    var game = gameService.gameCreateData.backendValidatedGame;
    var socket = socketService.timerSocket;

    socket.on('update_timer',function(data){
      timer.startTime = data.startTime;
      timer.duration = data.duration;
      timer.transpired = data.transpired;
    });

    var pauseTime = function(){
      // TODO insert game id here
      // socket.emit('puase_timer',{ gameID : game.id, action : 'pause'} );
    };

    var resumeTime = function(){
      // socket.emit('resume_timer',{ gameID : game.id, action : 'resume'} );
    };

    timer.pauseTime = pauseTime;
    timer.resumeTime = resumeTime;

    return {
      timer : timer
    };

  }]);
