 Newsfilter is a tool that gather tweets from a list of twitter channels, concatenate them, and proccess them in order to
 give a sidescroll effect, like those stupid LED side-scrolling message displayers.
 Intended for use with the status bar XMobar, adaptable to any status bar able to show custom messages.
 


First you need to input your credentials of Twitter API. Anyone with a Twitter account can get them, google it.<br>
So, create `Credentials` text file on local repo folder. It should have four lines:

```
{ consumer key }
{ consumer secret }
{ access token key }
{ access token secret }

```

Compile scroller.cpp with `-pthread` and `-lrt` flag; 

`$g++ scroller.cpp -o scroller -pthread -lrt -std=c++11`

Scroller 
Last step of the setup:


```
append to commands:

   , Run CommandReader "/full/path/to/scroller 'python /full/path/to/newsfilter.py'" 

-- add that  to the template:

<action=`python /path/to/scroller/enterHyperlink.py`>%CommandReader%</action>

```


This is how you use it on XMobar. Scroller takes the command to run `newsfilter.py` as it's unique argument, so that's it.

`NewsChannels` file contais the channel list, tweak it.

If you run `enterHyperlink.py` anytime, a browser window will pop and open last shown tweet's link, if it contained any. This is not working atm xD

With that action defined at .xmobarrc you can also click on the scrolling text
to access that hyperlink.

There should be some versions of this same thing around the internets,
but yeah... this repo was inspired by SimCity 3000.
Good luck on enjoying this XD


