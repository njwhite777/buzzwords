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
      // 'host' : '192.168.1.5',
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

app.config(function($stateProvider,$urlRouterProvider,localStorageServiceProvider,$mdThemingProvider) {

  $mdThemingProvider.alwaysWatchTheme(true);
  $mdThemingProvider.theme('default')
   .primaryPalette('blue', {
     'default': '400', // by default use shade 400 from the pink palette for primary intentions
     'hue-1': '100', // use shade 100 for the <code>md-hue-1</code> class
     'hue-2': '600', // use shade 600 for the <code>md-hue-2</code> class
     'hue-3': 'A100' // use shade A100 for the <code>md-hue-3</code> class
   })
   // If you specify less than all of the keys, it will inherit from the
   // default shades
   .accentPalette('blue', {
     'default': '100' // use shade 200 for default, and keep all other shades the same
   })
   .warnPalette('red',{
     'default': '400',
     'hue-1' : 'A400'
   })
;

  $mdThemingProvider.theme('Sweet')
    .primaryPalette('pink',{
      'default' : '400',
      'hue-1': 'A200',
      'hue-2': 'A400'
    })
    .accentPalette('light-green', {
      'default': 'A400' // use shade 200 for default, and keep all other shades the same
    })
    .warnPalette('lime',{
      'default': 'A100'
    })

    .backgroundPalette('blue-grey',{
      'default' : '200'
    });

  // This is necessary!
  $urlRouterProvider.when("", "/");
  localStorageServiceProvider
 .setPrefix('buzzwordsApp');
 // localStorageServiceProvider
  // .setStorageType('sessionStorage');
  localStorageServiceProvider
  .setNotify(true, true);

    var mainState = {
     url: '/',
     // abstract: true,
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

   var observerState = {
     url: '/observer_turn',
     templateUrl: './views/_observer.html',
     controller: 'observerController'
   };

   var guesserState = {
     url: '/guesser_turn',
     templateUrl: './views/_guesser.html',
     controller: 'guesserController'
   };

   var tellerrolldieState = {
     url: '/roll_die',
     templateUrl :'./views/_tellerrolldieview.html',
     controller:'tellerrolldieviewController'
   };

   var tellerState = {
     url: '/teller_turn',
     templateUrl :'./views/_tellerturnview.html',
     controller:'tellerturnviewController'
   }

   var moderatorState = {
     url: '/moderator_turn',
     templateUrl : './views/_moderatorturnview.html',
     controller : 'moderatorController'
   };

   $stateProvider.state('root',mainState);
   $stateProvider.state('gameinitiatorwait',gameinitiatorwaitState);
   $stateProvider.state('gameplayerwait',gameplayerwait);
   $stateProvider.state('observer',observerState);
   $stateProvider.state('guesser',guesserState);
   $stateProvider.state('tellerrolldie',tellerrolldieState);
   $stateProvider.state('teller',tellerState);
   $stateProvider.state('moderator',moderatorState);
});
