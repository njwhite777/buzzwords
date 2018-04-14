angular.module('frontendApp')
  .directive('buzzcards',['timerService','cardService','currentGameService','$timeout',function(timerService,cardService,currentGameService,$timeout){

    function link(scope, element, attrs){
      scope.cardData = cardService.cardData;
      scope.role = attrs.role;
      scope.cardService = cardService;
      scope.currentTurn = currentGameService.currentTurn;
    }

    return {
      restrict: 'E',
      link : link,
      template: '<div layout-align="center center" ng-show="currentTurn.turnState==\'initializing\'" class="text-med">Waiting to start turn.</div>' +
                '<div layout-align="center center" ng-show="currentTurn.turnState==\'finished\'" class="text-med">Turn Over!</div>'+
                '<md-card ng-if="cardData.showCard && currentTurn.turnState==\'running\'" class="card-slide" md-theme="{{ showDarkTheme ? \'dark-blue\' : \'default\' }}" md-theme-watch style="width: 400px;height=250px;">'+
                '  <md-card-title>'+
                '    <md-card-title-text>' +
                '       <span class="md-headline text-med"> {{ cardData.card.buzzword }} </span>'+
                '       <span ng-repeat="forbiddenword in cardData.card.forbiddenwords" class="text-medsmall" > {{ forbiddenword }} </span>'+
                '    </md-card-title-text>'+
                '  </md-card-title>'+
                '  <md-card-actions layout="row" layout-align="end center">'+
                '    <md-button ng-if="role==\'teller\'" ng-click="cardService.skipCard()" class="md-primary" >Skip Card</md-button>'+
                '  </md-card-actions>'+
                '</md-card>'
    };
}]);
