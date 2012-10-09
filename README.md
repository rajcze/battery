## battery

Battery is a simple sampler (or rompler if you wish) you can control only with keyboard. In fact only with couple keys. The goal was to have something to play samples I can control on a headless machine (I'm using [Rasberry Pi](http://www.raspberrypi.org/) and [MakeyMakey](http://www.makeymakey.com/) to control it right now). The philosophy is quite straightforward. Get some samples, copy them into samples directory and stick them into banks config file (right now only one is supported - see banks/default.json). You can specify as many banks as you want.

Once you've started the sampler you can switch banks with `space`. Use `w` to toggle sample reversing on and off. `a`, `s`, `d`, `f`, `g`, `h`, `j` and `arrow keys` are free slots you can use for your samples. These keys are almost everything MakeyMakey has in stock setting. To close the sampler press `q` or `ESC`.

I use curses for UI and key grabbing and pygame for audio output.


## todo

- refactor
- better UI
- banks conf file switching w/ cli args
- get rid of hardcoded values
- maybe get rid of pygame (quite too heavy dep)
- maybe some basic sound effects or DSP?