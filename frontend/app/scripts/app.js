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
    'ui.router'
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
        }
    });

app.config(function($stateProvider) {

    var main = {
      name: 'main',
      url: '',
      views: {
        'appmenu' : {
          name: 'appmenu',
          templateUrl: './views/_appmenu.html',
          controller: 'appmenuController'
        },
        'appscreen' : {
          name: 'appscreen',
          templateUrl: './views/_appscreen.html',
          controller: 'appscreenController'
        },
        'appscreen.gamemenuview' : {
          name: 'gamemenuview',
          templateUrl: './views/_gamemenuview.html',
          controller: 'gamemenuviewController'
        },
        'gameinitiatorview':{
          name: 'gameinitiatorview',
          templateUrl: './views/_gameinitiatorview.html',
          controller: 'gameinitiatorviewController'
        },
        'gameplayerturnview':{
          name: 'gameplayerturnview',
          templateUrl:"./views/_gameplayerturnview.html",
          controller: 'gameplayerturnviewController'
        },
        'gameplayerwaitview':{
          name: 'gameplayerwaitview',
          templateUrl:"./views/_gameplayerwaitview.html",
          controller: 'gameplayerwaitviewController'
        },
        'moderatorturnview':{
          name: 'moderatorturnview',
          templateUrl:"./views/_moderatorturnview.html",
          controller: 'moderatorturnviewController'
        },
        'tellerrolldieview':{
          name: 'tellerrolldieview',
          templateUrl:"./views/_tellerrolldieview.html",
          controller: 'tellerrolldieviewController'
        },
        'tellerturnview':{
          name: 'tellerturnview',
          templateUrl:"./views/_tellerturnview.html",
          controller: 'tellerturnviewController'

        }
      }
    };
    $stateProvider.state(main);
  });
