![node](http://blog.phusion.nl/wp-content/uploads/2013/10/nodelogo.png)
![GDG prototype](http://angularjs.org/img/AngularJS-large.png)

So having done the very basic form of interaction with a webcam, I was curious to see what else could be done. A lot of art exhibits just tend to show you things and the interaction (if any) can be quite limited. So I wanteded to push this a bit not just allowing people to change things directly themselves but also making it accessible to everyone.

This is when I got the idea of writing a simple web application which could be used to control the live performance software. This is where node.js came in. With the Express.js library I had a very simple JSON api up and running very quickly. For the moment, I just focused on that and tested it. I'm generally in favour of writing the API first as it will allow me or others to write all kinds clients later.

Having tested the API in node, I wanted to actually have ordinary people be able to use it (without even knowing what it is). So I started writing a static site which is being served up by node. To get the data from json to html forms and back again, angular was really useful.

Here are some screenshots of the configuration UI:

![GDG prototype](project_images/webscreen1.png)

![GDG prototype](project_images/webscreen2.png)

By the end of two evenings the node server now was serving up a configuration UI and was ready to relay that data to the Python program (which handles the camera and displaying the painting).



