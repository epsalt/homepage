---
type:
title: D3 Running Map
date:
url: running-map
tags:
---

<script src="//d3js.org/d3.v4.min.js"></script>
<script src="//d3js.org/d3-tile.v0.0.min.js"></script>
<link rel="stylesheet" type="text/css" href="/css/map.css">

This map contains data from about 200 runs recorded with
[Strava][strava] around Calgary, Canada. The longest run is from the
[2017 Calgary Marathon][marathon]. All the code for this visualization
is on [GitHub][github]. For more information check out the
accompanying [blog post][blog].

<svg id="running-map" viewBox="0 0 600 450" preserveAspectRatio="xMidYMid"></svg>
<script src="/js/running_map.js"></script>

## About

- Tiles copyright [OpenStreetMap contributors][osm].
- Built with [D3.js][d3]
- Map tiling code from [this example][tile].
- Inspired by [The America's Cup Finale: Oracle's Path to
Victory][oracle-cup] and the [Strava Global Heatmap][strava-heatmap].

[strava]: https://www.strava.com/athletes/22024093)
[blog]: /2018/01/running-map
[marathon]: https://www.startlinetiming.com/en/races/2017/calgarymarathon/view/2172
[github]: https://www.github.com/epsalt/d3-running-map
[osm]: https://www.openstreetmap.org/copyright
[d3]: https://d3js.org/
[tile]: http://bl.ocks.org/mbostock/eb0c48375fcdcdc00c54a92724733d0d
[oracle-cup]: http://www.nytimes.com/interactive/2013/09/25/sports/americas-cup-course.html
[strava-heatmap]: https://labs.strava.com/heatmap/#13.00/-114.07204/51.04448/blue/run
