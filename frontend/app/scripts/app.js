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
