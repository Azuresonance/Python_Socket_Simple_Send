# Python_Socket_Simple_Send
TCP sockets are troublesome to deal with.
Sometimes you just want to send a simple stuff, but since TCP is a stream-based protocol, you have to write all sorts of loops and buffering.
 to deal with TCP fragmenting your stuff.

This piece of code can reliably send your stuff and makes sure it arrives at the other side in one piece.

Anything that pickle can deal with is supported.
