---
type: project
template: project
title: Daylight Chart
date:
url: daylight
tags:
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/suncalc/1.8.0/suncalc.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.26.0/moment.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment-timezone/0.5.31/moment-timezone-with-data.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/5.9.1/d3.min.js"></script>
<script src="https://unpkg.com/leaflet@1.4.0/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/leaflet-geometryutil@0.9.1/src/leaflet.geometryutil.min.js"></script>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.4.0/dist/leaflet.css">
<link rel="stylesheet" type="text/css" href="/css/daylight.css">

Explore how daylight hours change throughout the year in locations
across the globe. Tap or hover over different points to update the
daylight contour plot below. If you are viewing on desktop, click to
lock the selected location.

<div class="wrapper">
    <div id="map"></div>
    <div id="chart"></div>
    <div id="legend"></div>
</div>

<script src="/js/daylight.js"></script>

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
