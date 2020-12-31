import { tzMap, sunChart } from './daylight/daylight.js';

const init  = {
    loc: "Atlantic/Madeira",
    lat: 32.6333,
    lon: -15.1,
    year: new Date().getFullYear()
};

const updateSunchart = sunChart(init.lat, init.lon, init.loc, init.year);
tzMap(updateSunchart);
