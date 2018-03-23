#!/usr/bin/env node
var SearchProvider = require( 'deepstream.io-provider-search-rethinkdb' );

var searchProvider = new SearchProvider({
  //optional, defaults to 'search'
  listName: 'query',

  logLevel: 3,

  // deepstream
  deepstreamUrl: 'localhost:6020',
  deepstreamCredentials: { username: 'rethinkdb-search-provider' },
  rethinkdbConnectionParams: {
      host: 'localhost',
      port: 28015,
      db: 'buzzwords'
  },
});

// and start it
searchProvider.start();

// it can also be stopped by calling
// searchProvider.stop();
