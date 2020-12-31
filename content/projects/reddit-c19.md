---
type: project
template: project
title: COVID-19 Discussion Trends
date: 2020-06-22 20:00:00 -0700
upated: 2020-06-22 20:00:00 -0700
slug: reddit-c19
thumb: reddit-c19/twitter.png
source: https://github.com/epsalt/reddit-c19-analysis
tags:
summary: My entry in the Alberta Innovates COVID-19 Datathon. An
	exploration of how discussion of topics related to the pandemic
	evolved from January to May 2020.
---

<div uk-alert class="uk-alert-primary">
This project was my entry into the Alberta Innovates 
<a
href="https://albertainnovates.ca/impact/newsroom/covid-19-hackathon/">COVID-19
Data Science Hackathon</a>. It won a <a href="https://albertainnovates.ca/impact/newsroom/flattening-the-curve-and-promoting-economic-recovery-through-innovation/">prize</a>
for best individual effort!
</div>

The project explored how Albertan discussion of the pandemic evolved
from January to May 2020 using data from ~500k comments on local
subreddits. An unsupervised text classification model was used to
determine if comments were relevant to a set of topics related to the
pandemic.

**Check out the notebook on [nbviewer][notebook] and the source
code on [Github][repo].**

![C19 Reddit Analysis Chart][chart]

## Tech

- **Data processing**: `dask` `numpy` `pandas` `spacy`
- **Modeling**: `gensim`
- **Visualization**: `altair`

## Acknowledgements

- Reddit data sourced from [pushshift.io][pushshift]
- Thanks to Alberta Innovates for hosting the Hackathon

[notebook]: https://nbviewer.jupyter.org/github/epsalt/reddit-c19-analysis/blob/master/c19-reddit-alberta.ipynb
[repo]: https://github.com/epsalt/reddit-c19-analysis
[pushshift]: https://pushshift.io/

[chart]: /images/reddit-c19/chart.svg
