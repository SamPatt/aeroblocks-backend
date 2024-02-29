# aeroblocks-backend

This is the backend for [Aeroblocks](https://aeroblocks.tech/), a React-based no-code configurator.

You can view the frontend code [here](https://github.com/SamPatt/aeroblocks).

## Technologies used

Aeroblocks uses a Flask server with MonogoDB (using MongoEngine). The server manages user authentication with JWT.

Code is lexed using Python's Abstract Syntax Tree (ast) module.

## User flow

### Register / login

`models.py` contains the `User` model, which stores users' profile information as well as a `canvases` property.

`canvases` contains a list of the users' canvases created with the `CanvasState` model.

#### Endpoints

Login: https://aeroblocks.tech/api/login

Register: https://aeroblocks.tech/api/register

### Code Lexing

When the user creates a new canvas, they're asking to upload code for lexing. A JSON object containing `blocks` is created from the output of running the code through Python's `ast` module.

This object is returned to the front end, which creates the grid and adds it to the blocks to generate the canvas state.

#### Endpoints

Create canvas: https://aeroblocks.tech/api/canvas/create

### Save / Load

The canvas state is maintained as a JSON object by the frontend, and can be saved to the user's profile in MongoDB.

The load endpoint will pull all canvases from the user's profile.

#### Endpoints

Save: https://aeroblocks.tech/api/canvas/save

Load: https://aeroblocks.tech/api/canvas/load