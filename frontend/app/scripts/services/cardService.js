'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:cardService
 * @description
 * # cardService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('cardService',['socketService','$timeout','debug',function(socketService,$timeout,debug){
    var socket = socketService.cardSocket;


    // var otherCards = [{buzzword:'alphabet1',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet2',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet3',forbiddenwords : ['a','b','c','d','notes 1123'] }];
    var cardData = { card : { buzzword : 'test', forbiddenwords : ['1','2','3','4'] }, showCard : false };

    var skipCard = function(){
      console.log("TODO: call backend for next card.")
      nextCard();
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
      console.log("TODO: implement backend call to award point");
      nextCard();
    };

    var awardPenalty =  function(){
      console.log("TODO: implement backend call to awardPenalty");
      nextCard();
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
