# DCS Messages Size Editor

 Simple tool to edit the size of messages in the DCS UI.

![readme_screenshot](./screenshot.png)

# How to use

No installation is required.
Just [download the latest released dcs_mse.exe](https://github.com/fisadev/dcs_mse/releases), place it in your DCS installation folder (not in Saved Games, but the game installation folder), and then run the executable. 

TODO: add screenshot of the tool

# Paranoid mode

Don't trust the executable? If you know Python and Git, you can clone this repo, check the code, and run the source yourself too.
Run it using Python 3.10 or later and [UV](https://docs.astral.sh/uv/getting-started/installation/). You will need to specify the path to your DCS installation folder as an argument:

```bash
uv run dcs_mse.py "C:\Program Files\Eagle Dynamics\DCS World"
```
