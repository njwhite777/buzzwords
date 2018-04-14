angular.module('frontendApp')
  .directive('teampoints',[
    'currentGameService',
    'cardService',
    '$timeout',
    function(currentGameService,cardService,$timeout){

      function link(scope, element, attrs){
        scope.cardService=cardService;
        scope.awardPoint=cardService.awardPoint;
        scope.awardPenalty=cardService.awardPenalty;
        scope.teams=currentGameService.turnData.teams;

      }

      return {
        restrict: 'E',
        link : link,
        template:
          '<md-card ng-repeat="team in teams" md-theme="{{ showDarkTheme ? \'dark-purple\' : \'default\' }}" md-theme-watch style="width:400px;margin:0px;margin-top:2px;">'+
          '  <div layout="row">'+
          '    <md-button ng-disabled="!team.onDeck" ng-click="awardPenalty()" class="text-med md-raised md-primary" style="margin:0px;color:#ffffff;border-right: 1px solid #BBBBBB;" >-1</md-button>'+
          // '    <md-divider style="border-top-width: 0;border-right-width: 2px;border-right-style: solid black;height: 100%;" ></md-divider>'+
          '    <md-card-title>'+
          '      <md-card-title-text>'+
          '        <span class="md-headline">{{ team.name }}</span>'+
          '      </md-card-title-text>'+
          '    </md-card-title>'+
          '    <md-button ng-click="awardPoint()" class="text-med md-raised md-primary" style="margin:0px;color:#ffffff;border-left: 1px solid #BBBBBB;" >+1</md-button>'+
          '   </div>'+
          '</md-card>'
      };
    }
  ]);
