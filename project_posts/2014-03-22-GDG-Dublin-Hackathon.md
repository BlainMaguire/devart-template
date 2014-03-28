![GDG](http://www.impacthub.net/wp-content/uploads/2014/02/GDG-Logo-1140x407.png "GDG")

So I got up early on a Saturday to jump into coding a prototype which would utilize this new version of Whistler and use a live feed from a camera. That was my goal for the day.

A large part of the morning was spent evaluating various ways to integrate the Python code with the camera. It turns out there are many ways to do this. I went for Pygame in the end because I'm already familiar with it and it was quick to get up and running.

![GDG people](https://lh3.googleusercontent.com/-fHK0GWAO1FU/Uy1wH1j7jiI/AAAAAAAAWT4/rK_T5z3coNY/w972-h550-no/IMG_20140322_110734-MOTION.gif)

### Numpy arrays, Pygame Images and Python Imaging Library Images

So the original Whistler code uses Python Imaging Library image objects but the image from the camera is using the format for Pygame. I needed to bridge that gap between the two. Seems like just converting to Numpy arrays worked first time but it wasn't without a few strange bugs to fix (particularly around width/height and differnt bit depths).

### Early Prototype

So towards the end of the day, I waded through copious amounts of errors until I finally got a live version of Whistler, updating a window istead of an image on the file system. I played around with various values, like changing the rate for passing the new camera image to the library, to see how that affected performance. Lots of tweaking like that.

Here's a photo of me trying the early prototype, complete with a debug console in the background:

![GDG prototype](https://lh6.googleusercontent.com/-f7bXtbYz0Yk/Uy2nIxhOtMI/AAAAAAAAWTg/56SaewxVKBA/w1004-h568-no/IMG_20140322_144754.jpg)

All in all, it was a productive day and it did also motivate me to continue to work on the project more.




