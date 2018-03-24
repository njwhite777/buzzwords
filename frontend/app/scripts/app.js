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
      'host':'localhost',
      'port':5000,
      'proto':'http://',
      'namespace':'io',
      'gameSocketName': 'game',
      'viewSocketName': 'view',
      'timerSocketName': 'timer',
      'getSocketNameHelper' :
        function(){
          return this.proto + this.host + ":"+ this.port+"/"+this.namespace;
        },
      'getSocketName' :
        function(whichSocket){
          if(whichSocket == undefined){
            return this.getSocketNameHelper();
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
          templateUrl: './views/_appmenu.html',
          controller: 'appmenuController'
        },
        'gamemenuview' : {
          name: 'gamemenuview',
          templateUrl: './views/_gamemenuview.html',
          controller: 'gamemenuviewController'
        }
      }
    };
    $stateProvider.state(main);
  });
