'use strict';

// Thanks to:
// https://stackoverflow.com/questions/18247130/how-do-i-store-data-in-local-storage-using-angularjs

angular.module('frontendApp')
  .service('loginUser',['localStorageService','playerService', function(localStorageService,playerService) {

    return {
      username : null,
      email : null,
      storeUsername : function(username){
        localStorageService.set("username",username);
        this.username = username;
      },
      storeEmail : function(email){
        localStorageService.set("userEmail",email);
        this.email = email;
      },
      deleteUsername : function(){
        return localStorageService.remove("username");
      },
      deleteEmail : function(){
        return localStorageService.remove("userEmail");
      },
      getUsername : function(){
        return localStorageService.get("username");
      },
      getPlayerDetails : function(){
        return { username : this.username, email : this.email };
      },
      createNewPlayer : function(email,username){
        this.storeEmail(email);
        this.storeUsername(username);
        playerService.emitPlayerJoined(this.getPlayerDetails());
      },
      registeredEmailInStorage: function(){
        var storageEmail = localStorageService.get("userEmail");
        var storageUsername = localStorageService.get("username");
        if(storageEmail && storageUsername){
          this.email = storageEmail;
          this.username = storageUsername;
          playerService.emitPlayerJoined(this.getPlayerDetails());
          // TODO: Do lookup on server to verify/notify that the user is checking back in.
          return true;
        }
        return false;
      }
    };
  }]);
