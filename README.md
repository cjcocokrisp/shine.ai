# shine.ai
A Machine Learning Project that aims to identify shiny Pokémon using neural networks to automate shiny hunting. For testing, a 3DS with Custom Firmware (CFW) was used due to having the ability to be screen captured and controlled through a computer.

## Technology Used

- Tensorflow (For Model)
- 3DS with CFW (Snickerstream for streaming and Input Redirection for control)
- Discord.py ()

## Model

A Sequential Neural Network trained on images of the hunts. Examples of datasets can be seen in the `dataset` directory. I found that training the model based on screenshots from the game at different points was easier then trying to just train it with images of the Pokemon. The games background details impact a lot!

## Process

The point of making this model was to test if I could use it to automate shiny hunting on the 3DS. To do this CFW was used due to it allowing you to capture the stream and use input redirection to control the system through a controller. I used a Keyboard to XInput program to get this to work with PyAutoGUI. The following process was used to automate the hunts.

1. Train the model for the hunt.
2. Set up the hunt on 3DS and get set up with the input method used in `hunt.py`.
3. Connect Discord bot for updates. 
4. Turn on Snickerstream and Input Redirection for control through the computer. 
5. Have computer simulate the hunt. 

## Hunts Completed

Mudkip (ORAS Starter Hunt) in 534 Encounters \[[Video](https://www.youtube.com/watch?v=Q6rHSdnZnE8)\]

![Mudkip Hunt Image](https://media.discordapp.net/attachments/1108978937079545897/1109209001658433596/temp.png?ex=66c841a2&is=66c6f022&hm=7423ed1778a92e0effb06899e246fffa32681da61aec37f13657a3c16d45b654&=&format=webp&quality=lossless&width=362&height=216)

Froakie (XY Starter Hunt) in 1978 Encounters

![Froakie Hunt Image](https://media.discordapp.net/attachments/1107361780906348636/1117694705887629432/temp.png?ex=66c8ce0f&is=66c77c8f&hm=c964801cf74762c587fd2a465b29676e4d20d86dc7184404441d7e5f7c7cbcda&=&format=webp&quality=lossless&width=287&height=215)

Rowlet (USUM Starter Hunt) in 3598 Encounters

![Rowlet Hunt Image](https://media.discordapp.net/attachments/1107361801835913287/1115948826608554015/temp.png?ex=66c862d5&is=66c71155&hm=3531089de2f2c2653b7d4935f1a95527a7496d90fcb2c30ecb30940b6e8fbd2d&=&format=webp&quality=lossless&width=362&height=215)