---
type: project
template: project
title: D3 Running Map
date: 2018-01-13 18:00:00 -0700
updated: 2019-02-27 18:00 -0700
slug: running-map
thumb: running-map/twitter.png
source: https://github.com/epsalt/d3-running-map
summary: 200 run animation rendered in the browser with D3.js and Canvas.
js: runningMap
css: runningMap
---

This map contains data from about 200 runs recorded with
[Strava][strava] around Calgary, Canada. The longest run is from the
2017 Calgary Marathon. All the code for this visualization is on
[GitHub][github]. For more information check out the accompanying
[blog post][blog].

<figure>
	<div id="map-wrapper">
		<svg id="map-container"></svg>
		<canvas id="tracks"></canvas>
		<canvas id="points"></canvas>
		<div id="controls">
			<div style="font-family: monospace;" id="timer"></div>
			<div class="map-button" id="play-button">Pause</div>
			<div class="map-button" id="restart-button">Restart</div>
		</div>
	</div>
	<figcaption>
	Map tiles copyright <a
	href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors
	</figcaption>
</figure>

## About

- Built with [D3.js][d3]
- Map tiling code from [this example][tile], D3 + canvas idea and some
  code from [this article][d3-canvas].
- Inspired by [The America's Cup Finale: Oracle's Path to
Victory][oracle-cup] and the [Strava Global Heatmap][strava-heatmap].

[strava]: https://www.strava.com/athletes/22024093)
[blog]: /2018/01/running-map
[github]: https://www.github.com/epsalt/d3-running-map
[d3]: https://d3js.org/
[tile]: http://bl.ocks.org/mbostock/eb0c48375fcdcdc00c54a92724733d0d
[d3-canvas]: https://bocoup.com/blog/d3js-and-canvas
[oracle-cup]: http://www.nytimes.com/interactive/2013/09/25/sports/americas-cup-course.html
[strava-heatmap]: https://labs.strava.com/heatmap/#13.00/-114.07204/51.04448/blue/run
