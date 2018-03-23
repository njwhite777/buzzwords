'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('gameService',['socketFactory',function(socketFactory) {
    var games;
    // This service is responsible for keeping date on the game screen!


    return {
      'games' : games
    };

  }]);
