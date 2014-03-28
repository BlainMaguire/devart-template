The final piece in the puzzle was getting the Python program to listen for some JSON from node so that it updated itself with the new config while it was running.

Like with just grabbing frames from a webcam, there are many different options here. There are always a lot of questions here, such as should I spawn a thread or do some kind of interprocess communation? It's certainly not out of the question to use something like Celery or Gevent to do this kind of thing. My initial approach was to give Flask a go, start the server inside a thread. However, as I was in development mode it didn't seem to like that. I continued to try lots of quick solutions like this to no avail.

In the end, I realised that I don't need a full blown http server, especially since the program will likely only ever be recieving stuff from a single node server at a time. So wrote a very simple socket listener which parses out the json and updates the program. Confident it would work, I typed it in one go. For at least 20 minutes though I couldn't figure out why my socket listener was blocking the main loop from running. Then I remembered, I need to set the thread to be a Daemon thread!

Should there be a possiblity of multiple instances of the python software running (potentially on different machines), with the node.js server sending the config, I don't have to worry at all about maintaining state of the config for the Python programs, they just set the options they're told to set.

It was good to do a bit of network programming again and also learn about things like socket.io in Node (although it turns out I didn't have any need for it for the prototype in the end).

