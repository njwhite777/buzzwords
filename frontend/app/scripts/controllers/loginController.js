'use strict';

/**
 * @ngdoc function
 * @name buzzwordsApp.controller:loginController
 * @description
 * # loginController
 * Controller of the buzzwordsApp
 */
angular.module('frontendApp')
  .controller('loginController', [
    '$scope',
    '$mdPanel',
    'loginUser',
    '$stateParams',
    'playerService',
    loginController]);

function loginController ($scope,$mdPanel,loginUser,$stateParams,playerService){
  this._mdPanel = $mdPanel;
  this.disableParentScroll = false;
  this._validUser = loginUser;
  if(!loginUser.registeredEmailInStorage())
  {
    this.showDialog();
  }
  playerService.emitPlayerJoined();
  // playerService.
  // $scope.isEmailValid = function(){
    // if( /(.+)@(.+){2,}\.(.+){2,}/.test($scope.ctrl.user.email) ){
      // console.log("valid email");
      // return true;
// } else {
    // return false;
// }
  // }();

}

loginController.prototype.showDialog = function(){
  var position = this._mdPanel.newPanelPosition()
      .absolute()
      .center();

  var panelAnimation = this._mdPanel.newPanelAnimation()
    .openFrom( {top: document.documentElement.clientHeight / 2 - 250, left: -50} )
    .duration(200)
    .closeTo( {top:  document.documentElement.clientHeight / 2 - 250, left: document.documentElement.clientWidth } )
    .withAnimation(this._mdPanel.animation.SCALE);

  var config = {
    // attachTo: angular.element(document.body),
    controller:  RegisterPanelController,
    controllerAs: 'ctrl',
    disableParentScroll: this.disableParentScroll,
    templateUrl: 'views/_registerOverlay.html',
    hasBackdrop: true,
    panelClass: 'registerOverlay',
    position: position,
    trapFocus: true,
    zIndex: 200,
    clickOutsideToClose: false,
    escapeToClose: false,
    animation: panelAnimation,
    focusOnOpen: true
  };

  this._mdPanel.open(config);
};

var RegisterPanelController = function(mdPanelRef,loginUser){
  this._mdPanelRef = mdPanelRef;
  this._validUser = loginUser;
  this.user = {};

  var name = loginUser.getUsername();
  if(name){
    this.user.name = name;
  }
  console.log(this.loginPlayerForm);

};

RegisterPanelController.prototype.closeDialog = function() {
  var panelRef = this._mdPanelRef;

  panelRef && panelRef.close().then(function() {
    angular.element(document.querySelector('.demo-dialog-open-button')).focus();
    panelRef.destroy();
  });
  this._validUser.storeEmail(this.user.email);
  this._validUser.storeUsername(this.user.name);
};
