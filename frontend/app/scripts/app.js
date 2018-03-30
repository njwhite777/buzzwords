'use strict';

/**
 * @ngdoc overview
 * @name frontendApp
 * @description
 * # frontendApp
 *
 * Main module of the application.
 */
var app = angular
  .module('frontendApp', [
    'btford.socket-io',
    'ngMaterial',
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ui.router',
    'LocalStorageModule'
  ]);

app
  .constant('debug', true )
  .constant('socketIOConfig',
    {
      'host' : 'localhost',
      'port' : 5000,
      'proto' : 'http://',
      'namespace' : 'io',
      'gameSocketName' : 'game',
      'viewSocketName' : 'view',
      'timerSocketName' : 'timer',
      'playerSocketName' : 'player',
      'getSocketNameHelper' :
        function(){
          return this.proto + this.host + ":"+ this.port+"/"+this.namespace;
        },
      'getSocketName' :
        function(whichSocket){
          if(whichSocket == undefined){
            return this.getSocketNameHelper();
          }
          if(whichSocket == 'view'){
            return this.getSocketNameHelper() + '/' + this.viewSocketName;
          }
          if(whichSocket == 'game'){
            return this.getSocketNameHelper() + '/' + this.gameSocketName;
          }
          if(whichSocket == 'timer'){
            return this.getSocketNameHelper() + '/' + this.timerSocketName;
          }
          if(whichSocket == 'player'){
            return this.getSocketNameHelper() + '/' + this.playerSocketName;
          }
        }
    });


app.run(function($rootScope) {
  $rootScope.$on("$stateChangeError", console.log.bind(console));
});

app.config(function($stateProvider,$urlRouterProvider,localStorageServiceProvider) {

  localStorageServiceProvider
 .setPrefix('buzzwordsApp');
 // localStorageServiceProvider
  // .setStorageType('sessionStorage');
  localStorageServiceProvider
  .setNotify(true, true);

    var mainState = {
     url: '/',
     views :
     {
        "appmenu@" : {
          parent: 'root',
          templateUrl:'./views/_appmenu.html',
          controller: 'appmenuController'
        },
        '':{
          parent: 'root',
          templateUrl: './views/_gamemenuview.html',
          controller: 'gamemenuviewController'
        }
      }
   };

   var gameplayerwait = {
     url: '/waitforgame',
     templateUrl : './views/_gameplayerwaitview.html',
     controller: 'gameplayerwaitviewController'
   }

   var gameinitiatorwaitState = {
     url: '/waitforplayers',
     templateUrl : './views/_gameinitiatorview.html',
     controller: 'gameinitiatorviewController'
   }

   var gameplayerturnState = {
     url: '/play_turn',
     templateUrl: './views/_gameplayerturnview.html',
     controller: 'gameplayerturnviewController'
   };

   var tellerrolldieState = {
     url: '/roll_die',
     templateUrl :'./views/_tellerrolldieview.html',
     controller:'tellerrolldieviewController'
   };

   var tellerturnState = {
     url: '/play_teller_turn',
     templateUrl :'./views/_tellerturnview.html',
     controller:'tellerturnviewController'
   }

   var moderatorturnState = {
     url: '/play_moderator_turn',
     templateUrl : './views/_moderatorturnview.html',
     controller : 'moderatorturnviewController'
   };

   $stateProvider.state('root',mainState);
   $stateProvider.state('gameinitiatorwait',gameinitiatorwaitState);
   $stateProvider.state('gameplayerwait',gameplayerwait);
   $stateProvider.state('gameplayerturn',gameplayerturnState);
   $stateProvider.state('tellerrolldie',tellerrolldieState);
   $stateProvider.state('tellerturn',tellerturnState);
   $stateProvider.state('moderatorturn',moderatorturnState);
});
