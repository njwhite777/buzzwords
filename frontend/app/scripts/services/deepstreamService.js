app.service('deepstreamService', function() {
          /************************************
          * Connect and login to deepstreamHub
          ************************************/
          //establish a connection. You can find your endpoint url in the
          //deepstreamhub dashbo
         return deepstream( 'localhost:6020' ).login();
})
