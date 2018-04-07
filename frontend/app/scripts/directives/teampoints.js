angular.module('frontendApp')
  .directive('teampoints',['cardService','$timeout',function(cardService,$timeout){

    function link(scope, element, attrs){
      scope.teams=[{id:22,name:'Teamcool',onDeck:true},{id:20,name:'othercool'}];
      scope.cardService=cardService;

    }

    return {
      restrict: 'E',
      link : link,
      template:
        '<md-card ng-repeat="team in teams" md-theme="{{ showDarkTheme ? \'dark-purple\' : \'default\' }}" md-theme-watch style="width:400px;margin:0px;margin-top:2px;">'+
        '  <div layout="row">'+
        '    <md-button ng-disabled="!team.onDeck" ng-click="cardService.awardPenalty(team.id)" class="text-med md-raised md-primary" style="margin:0px;color:#ffffff;border-right: 1px solid #BBBBBB;" >-1</md-button>'+
        // '    <md-divider style="border-top-width: 0;border-right-width: 2px;border-right-style: solid black;height: 100%;" ></md-divider>'+
        '    <md-card-title>'+
        '      <md-card-title-text>'+
        '        <span class="md-headline">{{ team.name }}</span>'+
        '      </md-card-title-text>'+
        '    </md-card-title>'+
        '    <md-button ng-click="cardService.awardPoint(team.id)" class="text-med md-raised md-primary" style="margin:0px;color:#ffffff;border-left: 1px solid #BBBBBB;" >+1</md-button>'+
        '   </div>'+
        '</md-card>'
    };
}]);
