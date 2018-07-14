 Newsfilter is a tool that gather tweets from a list of twitter channels, concatenate them, and proccess them in order to
 give a sidescroll effect, like those stupid LED side-scrolling message displays.
 Intended for use with the status bar XMobar, adaptable to any status bar able to show custom messages.
 


First you need to input your credentials of Twitter API. Anyone with a Twitter account can get them, google it.<br>
So, create `Credentials` text file on local repo folder. It should have four lines:

```
{ consumer key }
{ consumer secret }
{ access token key }
{ access token secret }

```


Then modify `.xmobarrc` to read the newz: 

```
append to commands:

   , Run CommandReader "/path/to/newsfilterScroller.py" "newsfilter" 

-- add that  to the template:

%newsfilter%

```

The color and and action bindings to click on scrolling tweet and launch the browser on its link are specific for xmobar, structured like this:
```
<action=`enterHyperlink http://twitter.com/cx0v9c8x`><fc=#fff></fc></action>
```

To use on another status bar that shows output of commands should be a matter of modifying thix sintax, at `newsfilterScroller.py`.

`NewsChannels` file contais the channel list, tweak it.

If a scrolling tweet is clicked on, the browser will open the link thru `enterHyperlink.py`. 

This project was inspired by SimCity 3000.
Good luck on enjoying this XD


