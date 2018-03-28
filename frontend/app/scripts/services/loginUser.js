'use strict';

// Thanks to:
// https://stackoverflow.com/questions/18247130/how-do-i-store-data-in-local-storage-using-angularjs

angular.module('frontendApp')
  .service('loginUser',['localStorageService', function(localStorageService) {

    return {
      validateToken : function(token){
        // TODO: implement. Will need some backend functionality!
        return true;
      },
      validateEmail : function(email){
        // TODO: implement.  Will need some backend functionality!
        return true;
      },
      validateUser : function(token,email){
        // I know this would make some programmers cringe hardcore!
        if(token == undefined && email == undefined){
          // TODO: Retrieve email and token from local storage.
          // TODO: Check with server if email and token are valid.
          return this.registeredEmailInStorage() && this.validUserTokenInStorage();
        }
        return (this.validateToken(token) && this.validateEmail(email));
      },
      _debugStoreEmail : function(email){
        localStorageService.set("userEmail",email);
      },
      _debugStoreToken : function(token){
        localStorageService.set("userToken",token);
      },
      _debugDeleteEmail : function(){
        return localStorageService.remove("userEmail");
      },
      _debugDeleteToken : function(){
        return localStorageService.remove("userToken");
      },
      validUserTokenInStorage : function(){
        var storageTok = localStorageService.get("userToken");
        if(storageTok){
          // return this.validateToken(storageTok);
          return true;
        }
        return false;
      },
      registeredEmailInStorage: function(){
        var storageEmail = localStorageService.get("userEmail");
        if(storageEmail){
          // return this.validateEmail();
          return true;
        }
        return false;
      }
    };
  }]);
