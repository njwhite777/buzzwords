'use strict';

// Thanks to:
// https://stackoverflow.com/questions/18247130/how-do-i-store-data-in-local-storage-using-angularjs

angular.module('frontendApp')
  .service('loginUser',['localStorageService','$q', function(localStorageService,$q) {
    var username=null;
    var email=null;
    var deferred = $q.defer();

    var registeredEmailInStorage = function(){
      var storageEmail = localStorageService.get("email");
      var storageUsername = localStorageService.get("username");
      if(storageEmail && storageUsername){
        email = storageEmail;
        username = storageUsername;
        return true;
      }
      return false;
    };

    var storeUsername = function(username){
      localStorageService.set("username",username);
      username = username;
    };

    var storeEmail = function(email){
      localStorageService.set("email",email);
      email = email;
    };

    var createNewPlayer = function(email,username){
      storeEmail(email);
      storeUsername(username);
      if(registeredEmailInStorage())
        deferred.resolve({ username : username, email : email });
    };

    var waitForPlayerDetails = function(){
      if(registeredEmailInStorage()){
        return deferred.resolve({username : username, email : email });
      }else{
        return deferred.promise;
      }
    };

    var getPlayerDetails = function(){
      return { username : username, email : email };
    };

    return {
      username : username,
      email : email,
      storeUsername : storeUsername,
      storeEmail : storeEmail,
      getPlayerDetails : getPlayerDetails,
      createNewPlayer : createNewPlayer,
      registeredEmailInStorage:registeredEmailInStorage,
      waitForPlayerDetails: waitForPlayerDetails,
      deleteUsername : function(){
        return localStorageService.remove("username");
      },
      deleteEmail : function(){
        return localStorageService.remove("email");
      },
      getUsername : function(){
        return localStorageService.get("username");
      }
    };
  }]);
