# WSGIserver - Serving HTTP Requests
A minimalistic **Python WSGI server** capable of handling HTTP requests. 
WSGI (Web Service Gateway Interface) allows execution of applications designed on any framework (*Django*, *Flask*, etc.) without tweaking server code.

WSGI inerfaces between the framework and the server and allows framework inependent code execution.



## Demonstration

In the command prompt, navigate to the directory where the file ```server.py``` is stored and execute the following command. 


```console
>python server.py flaskapp:app
```

<img src="https://live.staticflickr.com/65535/48149638927_d34af5b4ec_o_d.jpg" width="700">



This should be following by trying to load up the page in the browser to see the response generated by the app ```flaskapp.py``` which is a Flask based application and is present in the same directory as the ```server.py``` file

Any custom app in any framework can be created and used to generate server side responses.

![](https://live.staticflickr.com/65535/48149540941_f5d562d358_o_d.jpg)



**Current Limitations**
-------------
Current implementation only allows serving one request at a time as the queue size for reuqests has been limited to 1. 


