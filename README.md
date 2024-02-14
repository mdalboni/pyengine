# PyEngine

This is a sample game engine created with Python and Pygame.


## Installation

You can clone this repo and use pip install on it from Git Hub directly.
```bash
pip install git+https://github.com/mdalboni/pyengine
```

## Usage

After installing the pip package, you can use the following command to run generate your sample game.

### Project Init
```bash
pyengine init <folder_name> "<your_game_name>"
```

### Run Game
```bash
cd <folder_name>
python .
```

### To build the game and its compressed data
```bash
cd <folder_name>
pyengine build --output <output_path> 
```


### Uncovered Use Cases or Limitations
- Selection the game resolution to build:
  - Actual behavior:
    - It has only the default image resolution.
  - How to fix it: 
    - I would create the folders for each supported resolution and then the user would select the resolution to build the game.
    - And based on the selected option in the CLI we do the binaries for that, but that would be a terrible solution for a game, the customer should have all the binaries and switch locally.
  - Option:
    - We could always use the highest resolution and then resize it on the customer side based on the customer's screen resolution.
    - Or we could share the folders with all the images and pick based on the resolution of the customer's screen.
- Not allowing the user to build just for a language:
  - Actual behavior:
    - The user can only build the game for all the languages.
    - The "compiled" app will have all assets in it's binary.
  - Option:
      - We could make the resource folder visible for the user and allow it to be downloaded thought the app as a plugin/extension.
- Not giving the platform option in the CLI:
  - Actual behavior:
    - The user can only build the game for the current platform he is running the script.
  - Issue:
    - I did not manage to make it work properly on Mac and it wasted a lot of my time.
    - PyInstaller does not support cross compile, so we would need to have the specific platform to build the game.
    - We could emulate the OS but that would take more time for this sample.