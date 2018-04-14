'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:cardService
 * @description
 * # cardService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('cardService',['socketService','$timeout','currentGameService','debug',function(socketService,$timeout,currentGameService,debug){
    var socket = socketService.cardSocket;
    var gameSocket = socketService.gameSocket;

    // var otherCards = [{buzzword:'alphabet1',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet2',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet3',forbiddenwords : ['a','b','c','d','notes 1123'] }];
    var cardData = { card : { buzzword : 'test', forbiddenwords : ['1','2','3','4'] }, showCard : false };

    var skipCard = function(){
      var data = {
        gameID : currentGameService.currentGame.gameID,
        turnID : currentGameService.currentTurn.team.turnID
      };
      socket.emit('skip_card',data);
    };

    var getNextCard = function(){
      socket.emit('load_next_card');
    };

    var nextCard =  function(card){
      cardData.showCard = false;
      $timeout(function(){
        Object.assign(cardData.card,card.card);
        cardData.showCard = true;
      },400);
    };

    gameSocket.on('report_score',function(){
      Object.assign(cardData,{ showCard : false });
    });

    var awardPoint =  function(teamID){
      var data = {
        gameID : currentGameService.currentGame.gameID,
        turnID : currentGameService.currentTurn.team.turnID,
        teamID : teamID
      };
      socket.emit('award_point',data);
    };

    var awardPenalty =  function(){
      var data = {
        gameID : currentGameService.currentGame.gameID,
        turnID : currentGameService.currentTurn.team.turnID
      };
      socket.emit('award_penalty',data);
    };

    socket.on('load_card',function(data){
      nextCard(data);
    });

    return{
      cardData : cardData,
      skipCard : skipCard,
      awardPoint:awardPoint,
      awardPenalty:awardPenalty
    }
}]);
