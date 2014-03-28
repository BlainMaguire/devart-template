I decided I wanted to enter devart late last month. I wasn't entirely sure what exactly it was I wanted to do. I had numerous ideas throughout this period. I dug out some old projects I had on my machine and began experimenting with them.

I started to gravitate towards the idea of trying to create something intricate and colorful. In particular, I played around with some of my older 'infinite painting' code to see what I could come up with.

Here is an old video:
https://www.youtube.com/watch?v=88JOPdSF8h4

And here is one of my experients:
https://www.youtube.com/watch?v=EAMRH5K8YXQ

Although I kept iterating and liked some of the results, I didn't really feel that they were fitting with the theme of pushing the boundries, so I basically went back to the drawing board.

It was around this time that I decided a more interactive piece of some kind might be more interesting and maybe there was something I could do around that.

Painterly rendering looked nice, although the standard approach for doing it has already been done a lot for the likes of video/camera/3d graphics.

So I dug up [Whistler](https://github.com/BlainMaguire/whistler "Github") which was just a Python script which did it rather differently.

Any painterly renderers I've come across always use textures (usually along splines for brush strokes) and creates a bunch those in one or more passes.

Whistler doesn't use textures at all, it uses bezier curved shapes. It is incremental and doesn't follow any particular order so it's not obvious to anyone watching it progress what it will paint next.

Here's a picture of me with it starting to work:

![Me](project_images/mewhistler.png?raw=true "Me")

I thought it might be interesting to see Whistler was only really meant to be run as a standalone script on static images. So my first step was to alter the script so it could be used as a module and begin considering dynamic images.

As a motivation for me to continue to work on this I registered for the devart hackathon at my local Google Developers Group in Dublin.




