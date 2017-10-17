 Newsfilter is a tool that gather tweets from a list of twitter channels, concatenate them, and proccess them in order to
 give a sidescroll effect, like those stupid LED side-scrolling message displayers.
 Intended for use with the status bar XMobar, adaptable to any status bar able to show custom messages.
 


First you need to input your credentials of Twitter API. So, create `Credentials` text file on local repo folder. It should have four lines:

```
{ consumer key }
{ consumer secret }
{ access token key }
{ access token secret }

```

Then add a symlink to newsfiltershow to your PATH. Its an bash script that reads and deletes the first chars of the previously saved message (YES, thats how it works xD)
That bash script keeps cropping the message file (standard location is `~/.scroll`) until it's empty. Then it calls newsfilter.py to fill it again with fresh news. So 
you should also put a symlink to newsfilter.py on your path as `newsfilter`.

Last step of the setup:

On .xmobarrc:
```
append to commands:

   , Run Com "newsfiltershow" [] "newsfilter" 3


then add to the template:

%newsfilter%
```

This is how you use it on XMobar. For other status bars or uses, adapt it somehow.

If you run `openInfo.py` anytime, a browser window will pop and open last shown tweet's link, if it contained any. This should not work properly.

Newsfilter is a highly experimental piece of software is and I'm working on it. Ideas are appreciated.

Good luck on enjoying this :x
