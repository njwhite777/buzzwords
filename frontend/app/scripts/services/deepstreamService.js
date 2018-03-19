app.service('deepstreamService', function() {
          /************************************
          * Connect and login to deepstreamHub
          ************************************/
          //establish a connection. You can find your endpoint url in the
          //deepstreamhub dashbo
         return deepstream( '10.193.18.77:6020' ).login();
})
