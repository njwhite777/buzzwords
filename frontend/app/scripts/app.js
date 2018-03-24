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
          }
    });

app.config(function($stateProvider) {

    var main = {
      name: 'main',
      url: '',
      views: {
        'menu' : {
          templateUrl: './views/_menu.html',
          controller: 'menuController'
        },
        'maincontent' : {
          name: 'maincontent',
          templateUrl: './views/_maincontent.html',
          controller: 'maincontentController'
        }
      }
    };
    $stateProvider.state(main);
  });
