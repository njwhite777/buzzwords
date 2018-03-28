'use strict';

/**
 * @ngdoc function
 * @name buzzwordsApp.controller:registerController
 * @description
 * # registerController
 * Controller of the buzzwordsApp
 */
angular.module('frontendApp')
  .controller('registerController', [ '$scope','$mdPanel','loginUser','$stateParams', registerController]);

function registerController ($scope,$mdPanel,validUser,$stateParams){
  console.log("HERE!!")
  this._mdPanel = $mdPanel;
  this.disableParentScroll = false;
  this._validUser = validUser;
  if(!validUser.validateUser()) this.showDialog();
}

registerController.prototype.showDialog = function(){
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
    zIndex: 150,
    clickOutsideToClose: false,
    escapeToClose: false,
    animation: panelAnimation,
    focusOnOpen: true
  };

  this._mdPanel.open(config);
};

var RegisterPanelController = function(mdPanelRef,validUser){
  this._mdPanelRef = mdPanelRef;
  this._validUser = validUser;
};

RegisterPanelController.prototype.closeDialog = function() {
  var panelRef = this._mdPanelRef;

  panelRef && panelRef.close().then(function() {
    angular.element(document.querySelector('.demo-dialog-open-button')).focus();
    panelRef.destroy();
  });
  console.log(this.user.name);
  console.log(this.user.email);
  // TODO: get rid of these when we are not debugging
  this._validUser._debugStoreEmail(this.user.name);
  this._validUser._debugStoreToken("deadbeef");
};
