# HouseSim.py

## HouseSim Discord Bot 
HouseSim is a Discord bot designed to simulate a house environment. Each room in the house corresponds to a Discord text and voice channel. Users can move between these rooms and interact with the environment. 
### Features: 
* Voice Channel Monitoring: Detects when a user moves between voice channels (rooms). 
* Text Commands: Users can send commands in text channels to perform actions like moving between rooms or checking their location
* Server Initialization: Provides commands to set up the server with required roles and channels based on a JSON configuration
* Dynamic Loading: The bot's "house" environment can be loaded dynamically from a JSON file. 
* Logging: Logs events like user movements, command usage, etc. Installation & Setup: 
* Token: The bot token should be stored in a token.txt file in the root directory. 
* Dependencies: This bot uses the discord.py library. Install it using pip: pip install discord.py
* Configuration: The house structure is loaded from a JSON file named house.json Modify this file to customize the house layout. 

### Commands: 
 * $test: To test if the bot is responsive. 
 * $loadserver: Load the server structure from the JSON file. 
 * $initserver [ID]: Initialize the server structure based on the JSON file. The ID is currently hardcoded. 
 * $location: Check your current location (room). 
 * $move [room]: Move to a specified room. 
 * $entergame: Join the game. Players will start at the doorstep. $knock: Under construction. 
### Functions: 
 * loadJson: Loads the house configuration from a given JSON file. UnderConstruction: Sends a message back which tells the user the command is currently under construction. 
 * joinGame: Adds a player to the game by giving them the "In doorstep" role. 
 * initHouse: Creates all required roles and text chats for the house based on the JSON configuration. 
 * clean: Remove all "In" roles and channels. Useful for server cleanup. Debug: Dumps debugging information about roles, channels, and house configuration. 
### Running the Bot: 
  Execute the Python script to start the bot. Ensure the Discord bot token is available in token.txt and the required dependencies are installed.
Note: This bot alters server roles and channels based on commands. Ensure you're okay with these modifications before running or use a test server. 
Disclaimer: Some functions are commented out and some features are under construction, further development may be required to achieve full functionality.
