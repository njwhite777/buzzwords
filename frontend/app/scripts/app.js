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


app.config(function($stateProvider) {

    var main = {
      name: 'main',
      url: '',
      views: {
        'appMenu' : {
          templateUrl: './views/_appmenu.html',
          controller: 'appmenuController'
        },
        'gameMenuView' : {
          name: 'gamemenuview',
          templateUrl: './views/_gamemenuview.html',
          controller: 'gamemenuviewController'
        }
      }
    };
    $stateProvider.state(main);
  });
