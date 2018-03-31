<div style="text-align: right"> Nathan White </div>
<div style="text-align: right"> Aron Kageza </div>
<div style="text-align: right"> Hanqing Guo </div>  
<div style="text-align: right"> CS690: Software Engineering </div>  
<div style="text-align: right"> Documentation </div>  
<div></div>

# CS690 Buzzwords Application  
The following documentation is intended to orient posterity to both the structure and services that are involved in running the Buzzwords application.  To give a high level description of our architecture, the Buzzwords application is designed to be a multiclient, real time application.  It is composed of three main components: the front-end application written with javascript and utilizing the Angular 1 framework; the gameLogic which is a client responsible for watching various game feeds and events and responding to them accordingly; and the database component.  This last component is incredibly important for the real time operation of our application and would not be possible without using services such as rethinkdb and deepstream.  

##### Main Components:
- frontendApp
- database
- gameLogic


## frontendApp
This project is generated with [yo angular generator](https://github.com/yeoman/generator-angular)
version 0.16.0.

##### Build & development

Run `grunt` for building and `grunt serve` for preview.

##### Frontend Testing

Running `grunt test` will run the unit tests with karma.


## backendApp


## Useful Online Documents:  
deepstream-Rethink: https://deepstreamhub.com/open-source/integrations/db-rethinkdb/  


## Resources:
Digital Clock: https://codepen.io/Dunner/pen/MYPKgz
