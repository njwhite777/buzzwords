<div style="text-align: right"> Nathan White </div>
<div style="text-align: right"> Aron Kageza </div>
<div style="text-align: right"> Hanquing Guo </div>
<div style="text-align: right"> 20180424 </div>
<div style="text-align: right"> Rev 1.0 </div>


README
=
### Introduction:
CS690 Buzzwords is a digital emulation of the game Taboo. It makes use of a highly decoupled frontend/backend architecture and leverages the strengths of websockets to provide a real-time, multi-client, user experience. It has been implemented in Python3 using the Flask framework for backend functionality and ECS6 with the Angualr1 framework for the frontend functionality.  UI functionality, style, and animations were provided by the excellent Angular material design library in conjunction with angular-animate.   

#### Hardware & System Requirements:
The application has been implemented as a web application, consequently, a network connected server is necessary.  The server should have at least 1 CPU and 4GB RAM.  The system requires a linux based operating system, but should be relatively straight forward to adapt to a windows environment.     

#### Functionality
The application presents first time users with a simple dialog and asks them to log in, establishing a user name and password. On the menu screen, a user can decide to join an existing game that shows up in the menu, or create a new game. Once a user has joined/created a game, and a game reaches a valid state, the game flow will begin and each player will be selected for a particular role in a given turn. Each turn, a new team is selected to be "on deck" and a player from that team is selected to be the teller.  A player from one of the other team is selected to be a moderator and all other players are assigned as observers or guessers depending on the team that is "on deck" or the turn modifier that has been assigned for a particular turn. Once a certain number of points has been achieved by a team, the game will conclude, showing scores and allowing players to return to the main menu.  

- For details setup details, consult the System Manual.
- For details for how to use the program, consult the Users Manual. 
