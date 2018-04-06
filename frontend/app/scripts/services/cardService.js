'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:cardService
 * @description
 * # cardService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('cardService',['socketService','$http','$q','debug',function(socketService,$http,$q,debug){
    // This service listens to the created game event and adds a new game to the list when one is created.
    var otherCards = [{buzzword:'alphabet1',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet2',forbiddenwords : ['a','b','c','d','notes 1123'] },{buzzword:'alphabet3',forbiddenwords : ['a','b','c','d','notes 1123'] }];
    var cardData = {card : {buzzword:'alphabet',forbiddenwords : ['a','b','c','d','notes 1123']} };


    var skipCard = function(){
      cardData.card = otherCards.pop();
    };

    var nextCard =  function(){
      cardData.card = otherCards.pop();
    };

    var awardPoint =  function(){
      console.log("TODO: implement backend call to award point");
    };
    var awardPenalty =  function(){
      console.log("TODO: implement backend call to awardPenalty");
    };

    return{
      cardData : cardData,
      skipCard : skipCard,
      nextCard:nextCard,
      awardPoint:awardPoint,
      awardPenalty:awardPenalty
    }

  }]);
