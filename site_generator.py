#!/usr/bin/env python

"""
Static site generator for epsalt.ca. Converts markdown documents to
html using markdown and jinja2. Generates archive and tag pages.
"""

from collections import defaultdict
from os import listdir, makedirs
from os.path import dirname, exists, join

from dateutil.parser import parse
from feedgen.feed import FeedGenerator
from markdown import Markdown
from jinja2 import FileSystemLoader, Environment

dirs = {
    'posts': 'content/posts/',
    'projects': 'content/projects',
    'root': 'content/root',
    'tag': 'content/tag',
    'templates': 'templates',
    'site': 'site/',
    'images': 'images/'
}

site = {
    'url': 'https://epsalt.ca/',
    'title': 'from the desk of e.p salt',
    'name': 'E.P Salt',
    'email': 'evan@epsalt.ca'
}

class SiteGenerator(object):
    def __init__(self, dirs, site, reader, renderer):
        self.dirs = dirs
        self.site = site
        self.read = reader().read
        self.render = renderer(dirs).render

    def publish(self):
        self.render_posts(self.dirs['posts'], 'post.html')
        self.render_tags()
        self.render_root(self.dirs['root'])
        self.render_projects(self.dirs['projects'], 'project.html')
        self.render_rss(self.posts, self.site, self.dirs)

    def render_posts(self, src_dir, template):
        self.posts = []
        for post_file in listdir(src_dir):
            content, meta = self.read(src_dir, post_file)
            self.posts.append(Post(content, meta))

        self.posts = sorted(self.posts, key=lambda x: x.date, reverse=True)

        # Populate previous and next post attributes
        for post in self.posts:
            post.set_neighbours(self.posts)

        self.args = {'posts': self.posts}

        for post in self.posts:
            self.render(post, template, self.args, post.link)

        ## Render index
        index_args = self.args
        index_args['index'] = True
        self.render(self.posts[0], template, index_args, outpath='index.html')

    def render_tags(self):
        makedirs(join(self.dirs['site'], "tag"))

        tag_dict = defaultdict(list)
        for post in self.posts:
            for tag in post.meta.get('tags'):
                tag_dict[tag].append(post)

        for tag, tagged_posts in tag_dict.items():
            content, meta = "", {}
            page = Page(content, meta)
            args = {'posts': self.posts,
                    'tag_posts': tagged_posts,
                    'tag': tag}
            out = join("tag", tag)

            self.render(page, 'tag.html', args, out)

    def render_root(self, src_dir):
        for root_file in listdir(src_dir):
            content, meta = self.read(src_dir, root_file)
            page = Page(content, meta)
            url = page.meta.get('url')
            self.render(page, url + '.html', self.args, url)

    def render_projects(self, src_dir, template):
        for project in listdir(src_dir):
            content, meta = self.read(src_dir, project)
            page = Page(content, meta)
            self.render(page, template, self.args, page.meta.get('url'))

    def render_rss(self, posts, site, dirs):
        feed = FeedGenerator()
        feed.id(site['url'])
        feed.title(site['title'])
        feed.author({'name': site['name'], 'email': site['email']})
        feed.link(href=site['url'], rel="self")
        feed.language('en')

        for post in posts:
            post.set_rss_attributes(feed, dirs, site)

        feed.atom_file(join(dirs['site'], 'rss'), pretty=True)

class MarkdownReader(object):
    """ Reader for Markdown Files """

    def __init__(self):
        self.extensions = ['markdown.extensions.extra',
                           'markdown.extensions.meta',
                           'markdown.extensions.smarty']
        self.md = Markdown(self.extensions, output_format='html5')

    def read(self, directory, fname):

        path = join(directory, fname)

        with open(path, 'r') as f:
            html = self.md.convert(f.read())

            meta = {key: value if key == "tags" else value[0]
                    for key, value in self.md.Meta.items()}

        return html, meta

class JinjaRenderer(object):
    """ Renderer for Jinja2 templates """

    def __init__(self, dirs):
        self.site_dir = dirs['site']
        self.template_dir = dirs['templates']

    def render(self, page, template, args, outpath=None):
        """Method for rendering Pages with markdown and jinja2"""

        outpath = join(self.site_dir, outpath)

        args['post'] = page
        args['content'] = page.html

        # Create directory if necessary
        if not exists(dirname(outpath)):
            makedirs(dirname(outpath))

        # Use jinja to render template and save
        loader = FileSystemLoader(self.template_dir)
        env = Environment(loader=loader)
        text = env.get_template(template).render(args)
        with open(outpath, 'w') as outfile:
            outfile.write(text)

class Page(object):
    """ Base class for website pages """

    def __init__(self, html, meta):
        self.html = html
        self.meta = meta

class Post(Page):
    """ Pages with associated date and time """

    def __init__(self, content, meta):
        Page.__init__(self, content, meta)

        self.date = parse(self.meta.get('date'))
        self.directory = join(self.date.strftime('%Y'),
                              self.date.strftime('%m'))
        self.link = join(self.directory, self.meta.get('url'))
        self.ppost = None
        self.npost = None

    def set_neighbours(self, posts):
        """
        Sets next and previous post attributes.

        Given a list of Posts, this method sets the npost and ppost
        attributes. It is necessary that the post using this method
        be in the list, if it is not ValueError will be raised.

        """
        index = posts.index(self)

        # Check if the Post is last
        if index == 0:
            self.npost = None
        else:
            self.npost = posts[index-1]

        # Check if the post is first
        if index == len(posts)-1:
            self.ppost = None
        else:
            self.ppost = posts[index+1]

    def set_rss_attributes(self, feed, dirs, site):
        """
        Set RSS atrributes for a post.

        Given a python-feedgenerator object, this adds an entry for
        the post from the post content and metadata.

        """

        feed_entry = feed.add_entry()
        feed_entry.id(join(site['url'], self.link))
        feed_entry.title(self.meta.get('title'))
        feed_entry.published(self.date)
        feed_entry.updated(self.meta.get('updated'))

        # Full content with hardlinked images
        content = self.html.replace('src="/' + dirs['images'],
                                    'src="{}'.format(join(site['url'], dirs['images'])))
        feed_entry.content(content, type="html")

if __name__ == "__main__":
    generator = SiteGenerator(dirs, site, MarkdownReader, JinjaRenderer)
    generator.publish()
