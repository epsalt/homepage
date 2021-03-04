---
type: post
template: post
title: GitHub Code Search is Useful
date: 2021-03-03 19:00:00 -0700
updated: 2021-03-03 19:00:00 -0700
slug: github-code-search
tags:
  - github
summary: GitHub Search is surprisingly useful.
---

Searching through code is something most developers do every
day. Using `grep` to find occurrences of a string is a lot more
efficient than scrolling through every file in your project line by
line. Most modern editors have some kind of 'find in files'
functionality to do a regex search across your project.

Recently I have been getting a lot of utility out of [GitHub's
search][search] feature. Searching all of GitHub is like doing 'find
in files' on more than 215 million public repositories. It can be a
tremendous resource as long as you approach with a healthy amount of
caution. There is no quality enforcement of open source code uploaded
to the internet.

Here are a couple of things I have searched for recently:

- `use-package {package-name}` to see how other people have setup a
  specific package in their .emacs.d. The results helped me debug a
  tricky configuration problem and provided a lot of inspiration.

- `RequestFactory lanaguage:Python` to see how a part of the Django
  testing API is used in the wild.

If you end up using GitHub search often you can add it as a [custom
search engine][custom] in your browser with this URL:

```
https://github.com/search?q=%s&type=code
```

[search]: https://github.com/search
[custom]: https://support.google.com/chrome/answer/95426
