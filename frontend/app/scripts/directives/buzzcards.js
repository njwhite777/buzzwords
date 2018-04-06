angular.module('frontendApp')
  .directive('buzzcards',['timerService','cardService','$timeout',function(timerService,cardService,$timeout){

    function link(scope, element, attrs){
      scope.cardData = cardService.cardData;

      scope.role = attrs.role;

      scope.cardData.showCard = true;
      scope.cardService = cardService;

      scope.skipCard = function(){
        scope.cardData.showCard = false;
        $timeout(function(){
          cardService.skipCard();
          scope.cardData.showCard = true;
        },400);
      };
    }

    return {
      restrict: 'E',
      link : link,
      template: '<md-card ng-if="cardData.showCard" class="card-slide" md-theme="{{ showDarkTheme ? \'dark-blue\' : \'default\' }}" md-theme-watch style="width: 400px">'+
                '  <md-card-title>'+
                '    <md-card-title-text>' +
                '       <span class="md-headline text-med"> {{ cardData.card.buzzword }} </span>'+
                '       <span ng-repeat="forbiddenword in cardData.card.forbiddenwords" class="text-medsmall" > {{ forbiddenword }} </span>'+
                '    </md-card-title-text>'+
                '  </md-card-title>'+
                '  <md-card-actions layout="row" layout-align="end center">'+
                '    <md-button ng-if="role==\'teller\'" ng-click="skipCard()" class="md-primary" >Skip Card</md-button>'+
                '  </md-card-actions>'+
                '</md-card>'
    };
}]);
