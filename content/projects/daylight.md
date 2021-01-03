---
type: project
template: project
title: Daylight Chart
date: 2019-03-10 22:30:00 -0700
updated: 2020-05-27 22:00:00 -0700
slug: daylight
thumb: daylight/twitter.png
source: https://github.com/epsalt/daylight
summary: An interactive D3.js visualization of daylight hours around
	the world.
js: daylight
css: daylight
---

Explore how daylight hours change throughout the year in locations
across the globe. Tap or hover over different points to update the
daylight contour plot below. If you are viewing on desktop, click to
lock the selected location.

<div class="wrapper">
    <div id="map"></div>
    <div id="chart"></div>
    <div id="legend"></div>
</div>

## Notes

- Built with [D3][d3js], [SunCalc][suncalc], [Moment.js][moment], and
  [Leaflet][leaflet]
- With data from [Moment Timezone][mtz] and map tiles from
  [OpenStreetMap][osm]
- See the source code on [GitHub][github]
- Definitions of the different stages of twilight can be found
[here][twilight-wiki].
- [Read my blog post about this project][blog]

## Acknowledgment

This project was directly inspired by two sources, the excellent
daylight charts from [timeanddate.com][td.com] and an interactive map
of the world from the landing page of [Moment Timezone][mtz].

[twilight-wiki]: https://en.wikipedia.org/wiki/Twilight
[d3js]: https://d3js.org/
[suncalc]: https://github.com/mourner/suncalc
[moment]: http://momentjs.com/
[leaflet]: https://leafletjs.com/
[osm]: https://www.openstreetmap.org/
[mtz]: https://momentjs.com/timezone/
[td.com]: https://www.timeanddate.com/sun/canada/vancouver
[github]: https://github.com/epsalt/daylight
[blog]: /2019/03/daylight
