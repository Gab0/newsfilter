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

Compile scroller.cpp; resulting executable must be on same folder as newsfilter.py as long as you don't want to edit the cpp file (easy to find the path it searches).


Last step of the setup:

On add StdinReader to .xmobarrc: (Maybe it's already even there)
```
append to commands:

   , Run StdinReader

-- add that  to the template:

%StdinReader%
```

This is how you use it on XMobar. For other status bars, just enable their stdin reader, as scroller will send text to them thru pipe/stdin.

`NewsChannels` file contais the channel list, tweak it.

If you run `openInfo.py` anytime, a browser window will pop and open last shown tweet's link, if it contained any. This should not work properly.

Just run `scroller xmobar`. The bar process name shoud go as the first argument.

Newsfilter is a highly experimental piece of software is and I'm working on it. Ideas are appreciated.

Good luck on enjoying this :x
