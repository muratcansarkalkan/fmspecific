# Editing Stadium Editor assets

## Introduction
FIFA Manager games have 2 types of stadiums in 3D mode; default/custom stadiums and Stadium Editor stadiums.

## Default/custom stadiums

Default/custom stadiums have .o, .fsh, .loc and .bin files. Refer here for a detailed description.
https://github.com/muratcansarkalkan/fmspecific#file-convention-for-stadiums
We previously created tutorials for converting stadiums from other games, but they were in this format. In this article we will discuss editing Stadium Editor assets.
These stadiums will be referred as custom, while Stadium Editor stadiums will be referred as Editor from now on.

## Stadium Editor stadiums

All files related to stadiums can be found in data/stadium.

   ![FM Specific Tab](images/generic_1.png)
   
Content inside FIFA has custom stadiums for teams, represented with IDs. For instance, Arsenal’s ID is 000E0001, so in FIFA directory, there is a directory named 000E0001 and game loads the files. Usually the game loads custom stadium but when CPU teams/user team expands their stadium, it allows user to load either custom stadium, or Editor stadium in 3D Options section. The game also allows users to have Editor stadiums for teams. You can export Editor stadiums through Stadium Editor in-game. For example, if you created a replica for Franz-Horr-Stadion of Austria Wien in Stadium Editor and want to use it by default, you can save the file as 00040002 (ID of Austria Wien) in FIFA Manager/data/stadium.

   ![FM Specific Tab](images/generic_2.png)

If you want to load custom stadiums, you enable 2 options at the top. If not, Editor stadium will be in effect.

## Stadium Editor assets

Stadium Editor stadiums are technically very similar to custom stadiums. They use model and texture files. The difference is, there isn’t a compact model for these stadiums – files such as 000E0001 load a bunch of model pieces and textures to create a complete stadium. That file has location, rotation and scale data for stadium and environment models and information for what textures to be used.
The models and textures are inside the generator directory.

   ![FM Specific Tab](images/generic_3.png)

StadMain.big has all textures, while Stadelems.big has model files for all assets (tribunes, roof, flood lights, billboards, exterior assets such as buildings, trees).
In order to actually edit models we need to be delicate. A model file can be used my many stadiums. This limits our options. However with exterior we are more flexible.
