---
type: project
template: project
title: COVID-19 Discussion Trends
date:
slug: reddit-c19
tags:
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/vega/5.13.0/vega.min.js" integrity="sha256-5ANkOqHtTAtUSTOlF7znoJwGhGdGkzvgR+rrSFIpoFE=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vega-lite/4.13.1/vega-lite.min.js" integrity="sha256-gVLCkbJyEVv21r4PrvWDNV3mHUvt5HC8KVv9YHjLlPs=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vega-embed/6.9.0/vega-embed.min.js" integrity="sha256-6lWPqwalQ3ZXNwmeOFofejP1vAT81I5N23ZzA4JE4hI=" crossorigin="anonymous"></script>

This project was my entry into the Alberta Innovates [COVID-19 Data
Science Hackathon][hackathon]. It won a [prize for best individual
effort!][prize]

The project explored how Albertan discussion of the pandemic evolved
from January to May 2020 using data from ~500k comments on local
subreddits. An unsupervised text classification model was used to
determine if comments were relevant to a set of topics related to the
pandemic.

**Check out the notebook on [nbviewer][notebook] and the source
code on [Github][repo].**


<div id="vis"></div>

<script type="text/javascript">
	var spec = "/data/reddit-c19-chart.json"
	  vegaEmbed('#vis', spec).then(function(result) {
  }).catch(console.error);
</script>

## Technology

- **Data processing**: `dask` `numpy` `pandas` `spacy`
- **Modeling**: `gensim`
- **Visualization**: `altair`

## Acknowledgements

- Reddit data sourced from [pushshift.io][pushshift]
- Thanks to Alberta Innovates for hosting the Hackathon

[hackathon]: https://albertainnovates.ca/impact/newsroom/covid-19-hackathon/
[prize]: https://albertainnovates.ca/impact/newsroom/flattening-the-curve-and-promoting-economic-recovery-through-innovation/
[notebook]: https://nbviewer.jupyter.org/github/epsalt/reddit-c19-analysis/blob/master/c19-reddit-alberta.ipynb
[repo]: https://github.com/epsalt/reddit-c19-analysis
[pushshift]: https://pushshift.io/
