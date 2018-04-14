'use strict';
/**
 * @ngdoc function
 * @name frontendApp.controller:gameService
 * @description
 * # gameService
 * Controller of the left drawer of the application
 */

angular.module('frontendApp')
  .service('pointsService',['socketService','debug',function(socketService,debug){

    var socket = socketService.gameSocket;
    var teamScoreData = {};
    console.log("POINTS SERVICE INITIALIZED");

    socket.on('report_score',function(data){
      console.log("report_score",data);
      Object.assign(teamScoreData,data)
    });

    return {
      teamScoreData : teamScoreData
    };

}]);
