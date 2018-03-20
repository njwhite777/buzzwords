'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('gameService',['deepstreamService',function(ds) {
    const subscribeGameFeed = JSON.stringify({ table: 'games' ,query: [[ 'id','match','*']]});

    var games = {};

    var updateGameFeed = function(newGameData){
      console.log(newGameData);
    };

    const gameResult = ds.record.getList( 'search?' + subscribeGameFeed);
    gameResult.subscribe(updateGameFeed);
    console.log(gameResult);

    return {
      'games' : games
    };
    
  }]);
