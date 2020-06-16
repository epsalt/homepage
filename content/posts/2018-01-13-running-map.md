---
type: post
template: post
title: Revenge of Running Map
date: 2018-01-13 17:30:00 -0700
updated: 2018-01-18 00:30:00 -0700
slug: running-map
tag:
  - running
  - D3
  - javascript
  - python
summary: Using D3.js and Python to visualize running data.
---

About 200 runs around Calgary, visualized with [D3.js][d3]. See the
full interactive version [here][run] or check out the source code
on [GitHub][git].

![Running Map][runmap]
*Map tiles copyright [OpenStreetMap][osm-copyright] contributors*

I have been tracking my runs for a few years now, and have always
wanted to do something with the data. After a <span class="tip"
title="hence the 'revenge' in the title...">few iterations</span>,
this map is what I came up with. I have written below about my
inspiration for the visualization, some technical details, and a bit
of unnecessary evangelizing for the sport of running.

## On running

I am an on-again, off-again runner. I haven't been getting my
kilometers in for the past few months, but this time last year I was
starting to ramp my training up for the Calgary Marathon. Sports don't
come naturally to me, so completing a marathon is by far my biggest
athletic achievement to date.

Convincing yourself to get out running can be [difficult][casey] (my
recent dry spell is a testament to that). But it's worth it &mdash;
for the exercise, because sneakers are cheaper than a gym membership,
and to get to know a different side of your city.

## Visualization

Another reason to pick up running is the sweet, sweet data. If you use
an activity tracker, such as Strava or Runkeeper, then every time you
go on a run new data in the form of a GPS trace file is
generated. Most activity tracker apps allow you to painlessly export
your data out of the service. You can then do your own analysis, or in
this case, make maps.

A great example of visualizing activity data is the beautiful [Strava
global heatmap][heatmap]. I have used the global heatmap as a resource
when traveling to new and unfamiliar cities to aid in the search for
scenic and well-traveled running paths.

![Personal heatmap][heatm]
*My Strava [personal heatmap][p-heatmap]*

With a Strava premium subscription, you can generate your own
[personalized heatmap][p-heatmap]. This project started out as an
attempt to recreate my personal heatmap and improve my D3 skills in
the process.

Time and speed are an important part of running which you don't get to
see in the personal heatmap. My goal with this visualization was to
convey that motion. The inspiration for this came from the excellent
[America’s Cup Finale piece][oracle] by [Mike Bostock][mike] and [Shan
Carter][shan] for the [New York Times][nyt].

After adding movement, all the points start superimposed and then
venture out in different directions. This creates an effect similar to
a swarm of insects or a [Super Meat Boy victory sequence][meat]. The
heatmap is built up over time as all of the points move along their
routes.

## Implementation

The map is displayed in the browser using [D3.js][d3]. I have been
tinkering with the library for a few years, and this is my first
serious project. I relied heavily on a few examples to get going,
especially [this block][block] and viewing source on the [America's
Cup article][oracle] mentioned earlier. Broadly, the steps involved in
creating the visualization were:

1. Exporting [run data from Strava][export]
2. Writing a simple `.gpx` parser in Python (you could also
   use [gpx-py][gpx-py], but I wanted to write a simple parser as a
   learning exercise)
3. Resampling to a consistent time interval with [pandas][panda]
4. Visualizing the data in the browser using [D3.js][d3]

If you want to try creating a similar map with your own data, I've put
all the code and more detailed instructions on [GitHub][git].

## Performance

My biggest source of pain on this project has been performance and
frame rate. The position of each point has to be updated many times
per second for the animation to appear pleasantly smooth.

The usual D3 workflow consists of binding data to the DOM and
rendering SVG elements. This DOM integration is a reason why D3 is
powerful, but also imposes some limitations. Large amounts of nodes
result in [sluggish animations or browser crashes][performance-test].

I tried to get to a level of performance that I was happy with using
SVG rendering but was unsuccessful. Thankfully, I eventually stumbled
upon a [very helpful article by Irene Ros on working with D3 and
Canvas][d3-canvas]. Using canvas as a renderer is more appropriate for
my use case (many frequently updated nodes) and helped solve my
performance woes.

## To conclude

- See the full interactive version of the visualization [here][run].
- Running is great and you should try it. While you are struggling
  through that Sunday morning long run, just think about all the data
  you are generating.
- SVG rendering doesn't work well with many nodes, especially when
  elements are being frequently updated. Consider switching to canvas
  when performance becomes an issue.

[d3]: https://d3js.org
[git]: https://www.github.com/epsalt/d3-running-map
[osm-copyright]: http://www.openstreetmap.org/copyright
[run]: /projects/running-map
[casey]: https://youtu.be/oLXG6ITzLIo
[heatmap]: https://labs.strava.com/heatmap/#13.00/-114.07204/51.04448/blue/run
[p-heatmap]: https://www.strava.com/athletes/22024093/heatmaps/32b413d#12/51.04139/-114.03809
[oracle]: http://www.nytimes.com/interactive/2013/09/25/sports/americas-cup-course.html
[nyt]: http://www.nytimes.com
[mike]: https://bost.ocks.org/mike/
[shan]: http://shancarter.com/
[meat]: https://youtu.be/92R_5uuQltQ
[block]: http://bl.ocks.org/mbostock/eb0c48375fcdcdc00c54a92724733d0d
[export]: https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk
[gpx-py]: https://github.com/tkrajina/gpxpy
[panda]: https://pandas.pydata.org/
[osm]: http://www.openstreetmap.org
[performance-test]: http://tommykrueger.com/projects/d3tests/performance-test.php
[d3-canvas]: https://bocoup.com/blog/d3js-and-canvas

[runmap]: /images/running-map/running-map.gif
[heatm]: /images/running-map/personal-heatmap.png
