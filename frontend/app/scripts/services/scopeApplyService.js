'use strict';

angular.module('frontendApp')
  .service('scopeApply', function(){
    return function (scope) {
      if( !scope.$$phase ) {
        scope.$apply();
      }
    };
  });
