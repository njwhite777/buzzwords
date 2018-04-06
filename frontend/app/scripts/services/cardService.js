'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:cardService
 * @description
 * # cardService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('cardService',['socketService','$http','$timeout','debug',function(socketService,$http,$timeout,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.
    var otherCards = [{buzzword:'alphabet1',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet2',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet3',forbiddenwords : ['a','b','c','d','notes 1123'] }];
    var cardData = {card : {buzzword:'alphabet',forbiddenwords : ['a','b','c','d','notes 1123']},showCard: true };

    var skipCard = function(){
      console.log("TODO: implement backend call to move to next card.");
      nextCard();
    };

    var nextCard =  function(){
      cardData.showCard = false;
      $timeout(function(){
        cardData.card = otherCards.pop();
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

    return{
      cardData : cardData,
      skipCard : skipCard,
      awardPoint:awardPoint,
      awardPenalty:awardPenalty
    }
}]);
