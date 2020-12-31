import * as d3 from 'd3-4';
import { tile } from 'd3-tile';

import './running_map.css';

function runningMap() {
  var config = {
    "scale": 98304,
    "lat": 51.0375,
    "lon": -114.09,
    "fps": 15,
    "resampleInterval": 30,
    "trackWidth": 2,
    "circleWidth": 1,
    "radius": 2,
    "source": "/data/gpx_rollup.csv"
  };

  var canvasPoints = document.querySelector("canvas#points"),
      canvasTracks = document.querySelector("canvas#tracks"),
      contextPoints = canvasPoints.getContext("2d"),
      contextTracks = canvasTracks.getContext("2d"),
      detachedContainer = document.createElement("custom"),
      dataContainer = d3.select(detachedContainer);

  // initial dimensions
  canvasPoints.width = canvasPoints.offsetWidth;
  canvasPoints.height = canvasPoints.offsetHeight;

  canvasTracks.width = canvasTracks.offsetWidth;
  canvasTracks.height = canvasTracks.offsetHeight;

  var width = canvasPoints.offsetWidth,
      height = canvasPoints.offsetHeight;

  function changeResolution(canvas, context, scaleFactor) {
    // this function from https://stackoverflow.com/a/26047748
    canvas.style.width = canvas.style.width || canvas.width + 'px';
    canvas.style.height = canvas.style.height || canvas.height + 'px';

    canvas.width = Math.ceil(canvas.width * scaleFactor);
    canvas.height = Math.ceil(canvas.height * scaleFactor);
    context.scale(scaleFactor, scaleFactor);
  }

  // changes for mobile devices
  if (width < 480) {
    config.fps = 10;
    config.resampleInterval = 45;
    config.source = "/data/gpx_rollup45.csv";
    config.scale = 80000;
    changeResolution(canvasPoints, contextPoints, 2);
    changeResolution(canvasTracks, contextTracks, 2);
  }

  var projection = d3.geoMercator()
      .scale((config.scale) / 2 * Math.PI)
      .translate([width / 2, height / 2])
      .center([config.lon, config.lat]);

  var path = d3.geoPath()
      .projection(projection)
      .pointRadius(3.5)
      .context(contextTracks);

  var tiles = tile()
      .size([width, height])
      .scale(projection.scale() * 2 * Math.PI)
      .translate(projection([0, 0]))();

  d3.select("svg#map-container").selectAll("image")
    .data(tiles)
    .enter().append("image")
    .attr("xlink:href", function (d) { return "http://" + "abc"[d[1] % 3] + ".tile.openstreetmap.org/" + d[2] + "/" + d[0] + "/" + d[1] + ".png"; })
    .attr("x", function (d) { return (d[0] + tiles.translate[0]) * tiles.scale; })
    .attr("y", function (d) { return (d[1] + tiles.translate[1]) * tiles.scale; })
    .attr("width", tiles.scale)
    .attr("height", tiles.scale);

  var playButton = d3.select("#play-button"),
      restartButton = d3.select("#restart-button"),
      timer = d3.select("#timer");

  d3.csv(config.source, function (error, data) {
    if (error) { throw error; }

    data = data.map(function (d) { return [+d.lon, +d.lat, +d.index, +d.len]; });

    var nested = d3.nest()
	.key(function (d) { return d[2]; })
	.entries(data);

    var tracks = dataContainer.selectAll("custom.geoPath")
	.data(nested)
	.enter()
	.append("custom")
	.classed("geoPath", true);

    var runners = dataContainer.selectAll("custom.circle")
	.data(nested)
	.enter()
	.append("custom")
	.classed("circle", true);

    var maxElapsed = Math.max.apply(Math, (data.map(function (d) { return d[3]; })));

    var interval = 1000 / config.fps,
	t = 0,
	going = true,
	pct,
	time;

    function drawCanvas() {
      contextTracks.strokeStyle = "rgba(74,20,134,0.2)";
      contextTracks.lineWidth = config.trackWidth;

      tracks.each(function () {
	var node = d3.select(this),
            trackData = node.data()[0].values;

	if (t > 0 && t < trackData.length) {
          contextTracks.beginPath();
          path({type: "LineString", coordinates: [trackData[t-1], trackData[t]]});
          contextTracks.stroke();
	}
      });

      contextPoints.clearRect(0, 0, width, height);
      contextPoints.lineWidth = config.circleWidth;
      contextPoints.strokeStyle = "black";
      contextPoints.beginPath();

      runners.each(function () {
	var node = d3.select(this);
	contextPoints.moveTo(parseFloat(node.attr("x")) + parseFloat(config.radius), node.attr("y"));
	contextPoints.arc(node.attr("x") + config.radius, node.attr("y"), config.radius, 0, 2 * Math.PI);
      });

      contextPoints.stroke();
    }

    var coord_slicer = function (d, t) {
      return projection(d.values[Math.min(t, d.values[0][3] - 1)]);
    };

    function step(t) {
      runners
	.attr("x", function (d) { return coord_slicer(d, t)[0]; })
	.attr("y", function (d) { return coord_slicer(d, t)[1]; });

      time = new Date(null);
      time.setSeconds(t * config.resampleInterval);
      time = time.toISOString().substr(11, 5);
      pct = (t / maxElapsed * 100).toFixed(0);
      if (pct.length === 1) { pct = "0" + pct; }

      timer.text("Elapsed: " + time + "/" + pct + "%");

      drawCanvas(t);
    }

    function restart() {
      contextTracks.clearRect(0, 0, width, height);
      t = 0;
      step(t);
    }

    d3.interval(function () {
      if (t > maxElapsed) { restart(); }
      if (going) {
	step(t);
	t++;
      }
    }, interval);

    function pauseResume() {
      if (going) {
	playButton.text("Resume");
	going = false;
      } else {
	playButton.text("Pause");
	going = true;
      }
    }

    playButton.on("click", pauseResume);
    restartButton.on("click", restart);

  });
}

export { runningMap as default };
