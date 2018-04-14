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


    // var otherCards = [{buzzword:'alphabet1',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet2',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet3',forbiddenwords : ['a','b','c','d','notes 1123'] }];
    var cardData = { card : { buzzword : 'test', forbiddenwords : ['1','2','3','4'] }, showCard : false };

    var skipCard = function(){
      var data = {
        gameID : currentGameService.currentGame.gameID,
        turnID : currentGameService.currentTurn.team.turnID
      };
      console.log("PRESSED SKIP",data);
      console.log("PRESSED SKIP",currentGameService.currentTurn);
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

    var awardPoint =  function(){
      var data = {
        gameID : currentGameService.currentGame.gameID,
        turnID : currentGameService.currentTurn.turnID
      };
      console.log("AWARDING POINT:",data);
      socket.emit('award_point',data);
    };

    var awardPenalty =  function(){
      var data = {
        gameID : currentGameService.currentGame.gameID,
        turnID : currentGameService.currentTurn.turnID
      };
      console.log("AWARDING PENALTY:",data);
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
