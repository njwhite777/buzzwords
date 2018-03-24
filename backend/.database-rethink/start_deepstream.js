#!/usr/bin/env node
const Deepstream = require('deepstream.io')
const DSRethinkConnector = require("deepstream.io-storage-rethinkdb")

// Setup the deepstream server
const server = new Deepstream('./conf/config.yml')

server.set("storage", new DSRethinkConnector({
    port: 28015,
    host: "localhost",
    splitChar: "/",
    database: "buzzwords"
}));


const C = Deepstream.constants;

/*
The server can take
1) a configuration file path
2) null to explicitly use defaults to be overriden by server.set()
3) left empty to load the base configuration from the config file located within the conf directory.
4) pass some options, missing options will be merged with the base configuration
*/

// start the server
server.start()