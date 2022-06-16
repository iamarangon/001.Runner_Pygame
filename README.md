# Runner Game
 Basic 2D Runner Game

Game created following "ClearCode" tutorial from YouTube

- link to video: https://youtu.be/AY9MnQ4x3zk?list=PLsIbpk0M-XAlhSR7Bc6B7ef5h_PWkNA2B
- his project folder: https://github.com/clear-code-projects/UltimatePygameIntro

-----------------------

# To do later

1. Correct the way the game behave when it's over (game restarts simply by pressing SPACE button):
- Possible solutions:
    * Create a Game Over title with some new entry/behave (save high score/change the button to restart the game)

2. Save scores:
- I need to implement an entry in the Game Over Title to save the current score with a Player Name;
- Could either enter the Player Name in the Game Menu, before starting, or just entry it everytime the game ends;
- Use a json file to save it, so I can create a "High Score Menu" in the Game Menu;
    * Must save only a few scores (create a if condition to check if the value is higher than those already saved);