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
    var cardData = {card : {buzzword:'',forbiddenwords : ['','','','']},showCard: true };

    var skipCard = function(){
      console.log("TODO: implement backend call to move to next card.");
      nextCard();
    };

    var nextCard =  function(card){
      cardData.showCard = false;
      $timeout(function(){
        cardData.card = card;
        cardData.showCard = true;
      },400);
      console.log("TODO: implement backend call to move to next card.");
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
