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
    '$q',
    'currentGameService',
    'debug',
    function(socketService,gameService,$state,$q,currentGameService,debug){

      console.log("in timerService");
    // Timer is an object so that it can be utilized by our front end to update if need be.
    var timer = {
      status : "initializing",
    };

    var game = currentGameService.currentGame;
    var socket = socketService.timerSocket;

    socket.on('update_timer',function(data){
      console.log("UPDATE TIMER:",data);
      Object.assign(timer,data);
    });

    socket.on('timer_paused',function(data){
      Object.assign(timer,data)
    });

    socket.on('timer_resumed',function(data){
      Object.assign(timer,data);
    })

    var pauseTime = function(){
      socket.emit('pause_timer',{ gameID : game.id, action : 'pause'} );
    };

    var resumeTime = function(){
      socket.emit('resume_timer',{ gameID : game.id, action : 'resume'} );
    };

    timer.pauseTime = pauseTime;
    timer.resumeTime = resumeTime;

    return {
      timer : timer
    };

  }]);
