'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('currentGameService',['$q','socketService','debug',function( $q,socketService,debug ){

    var socket = socketService.gameSocket;
    var currentGame = {

    };

    var currentTurn = {
      roles:    {},
      team:     {},
      teams: {},
      modifier: {},
      assignedRole : {},
      turnState : 'initializing',
      card : {}
    };

    var deferred = $q.defer();

    var startGame = function(){
      socket.emit('start_game',currentGame);
    };

    var startTurn = function(){
      socket.emit("starting_turn",currentGame);
    };

    socket.on('turn_started',function(data){
      currentTurn['turnState'] = 'running';
    });

    socket.on('turn_finished',function(data){
      currentTurn['turnState'] = 'finished';
      currentTurn['card']['isPhrase'] = "";
    });

    socket.on('timer_finished',function(data){
      console.log("TIMER IS FINISHED",data)
      socket.emit('turn_complete',data);
    });

    socket.on('report_score',function(){
      console.log("REPORTED SCORE, RESETTING");
      Object.assign(currentTurn, {
        roles:    {},
        team:     {},
        teams: {},
        modifier: {},
        assignedRole : {},
        turnState : 'initializing'
      });
    });

    // The event listener which returns when your own game has been created.
    socket.on('created_your_game',function(data){
      setGame(data);
    });

    socket.on('joined_team',function(data){
      setGame(data);
    });

    // Sets the current game and resolves it imediately.
    var setGame = function(game){
      Object.assign(currentGame,game);
      deferred.resolve(game);
    }

    var getGame = function(){
      return deferred.promise;
    };

    socket.on('is_phrase',function(data){
      console.log("Card is phrase: ",data);
      Object.assign(currentTurn.card,data);
    });

    socket.on('turn_role_assignment',function(data){
      console.log("ROLE ASSIGNMENT:",data);
      Object.assign(currentTurn.assignedRole,data);
    });

    socket.on('turn_data',function(data){
      console.log("TURN DATA",data);
      Object.assign(currentTurn.roles,data['roles']);
      Object.assign(currentTurn.team,data['team']);
      Object.assign(currentTurn.teams,data['teams']);
    });

    socket.on('roll_result',function(data){
      Object.assign(currentTurn.modifier,data);
    });

    return {
      startGame : startGame,
      startTurn : startTurn,
      currentGame : currentGame,
      currentTurn : currentTurn,
      setGame : setGame,
      getGame : getGame
    };

}]);
