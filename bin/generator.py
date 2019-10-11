#!/usr/bin/env python3

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

DIRS = {
    'posts': 'content/posts/',
    'projects': 'content/projects',
    'root': 'content/root',
    'tag': 'content/tag',
    'templates': 'templates',
    'site': 'site/',
    'images': 'images/'
}

SITE = {
    'url': 'https://epsalt.ca/',
    'title': 'from the desk of e.p salt',
    'name': 'E.P Salt',
    'email': 'evan@epsalt.ca'
}


class SiteGenerator:
    """ Static Site generator class """

    def __init__(self, dirs, site, reader, renderer):
        self.dirs = dirs
        self.site = site
        self.read = reader().read
        self.render = renderer(dirs).render

    def publish(self):
        """ Method for rendering static site """

        posts = self.build_post_list(self.dirs['posts'])
        args = {'posts': posts}

        # Special cases
        self.render_pages(posts, args, out_dir = None)
        self.render_tags(posts)
        self.render_rss(posts, self.site, self.dirs)

        # General cases
        dir_dict = {
            "": self.dirs['root'],
            "projects": self.dirs['projects']
        }

        for out_dir, src_dir in dir_dict.items():
            pages = self.read_from_dir(src_dir, Page)
            self.render_pages(pages, args, out_dir)

        # Index
        index = posts[0]
        index_args = args
        index_args['index'] = True
        self.render(index, index.meta.get('template'), index_args, outpath='index.html')

    def read_from_dir(self, src_dir, page_class):
        """ Read all pages in a directory to page_class """

        pages = []
        for page in listdir(src_dir):
            content, meta = self.read(src_dir, page)
            pages.append(page_class(content, meta))

        return pages

    def build_post_list(self, post_dir):
        """ Build list of all posts in post_dir """

        posts = self.read_from_dir(post_dir, Post)

        sorted_posts = sorted(posts, key=lambda x: x.date, reverse=True)

        for post in sorted_posts:
            post.set_neighbours(sorted_posts)

        return sorted_posts

    def render_pages(self, pages, args, out_dir):
        """ Render all pages in a list with given template args """

        for page in pages:
            page_type = page.meta.get('type')
            template = page.meta.get('template')

            if page_type == 'post':
                out = page.link
            else:
                out = join(out_dir, page.meta.get('url'))

            self.render(page, template, args, out)

    def render_tags(self, posts):
        """ Build tag list and render tag pages """

        makedirs(join(self.dirs['site'], "tag"))

        tag_dict = defaultdict(list)
        for post in posts:
            for tag in post.meta.get('tags'):
                tag_dict[tag].append(post)

        for tag, tagged_posts in tag_dict.items():
            content, meta = "", {}
            page = Page(content, meta)
            args = {'posts': posts,
                    'tag_posts': tagged_posts,
                    'tag': tag}
            out = join("tag", tag)

            self.render(page, 'tag', args, out)

    def render_rss(self, posts, site, dirs):
        """ Build and render RSS feed for given post list """

        feed = FeedGenerator()
        feed.id(site['url'])
        feed.title(site['title'])
        feed.author({'name': site['name'], 'email': site['email']})
        feed.link(href=site['url'], rel="self")
        feed.language('en')

        for post in posts:
            post.set_rss_attributes(feed, dirs, site)

        feed.atom_file(join(dirs['site'], 'rss'), pretty=True)


class Page:
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


class MarkdownReader:
    """ Reader for Markdown Files """

    def __init__(self):
        self.extensions = ['markdown.extensions.extra',
                           'markdown.extensions.meta',
                           'markdown.extensions.smarty',
                           'markdown.extensions.codehilite']
        self.md = Markdown(self.extensions, output_format='html5')

    def read(self, directory, fname):
        """ Read a markdown file and convert to HTML """

        path = join(directory, fname)
        with open(path, 'r') as f:
            html = self.md.convert(f.read())
            meta = {key: value if key == "tags" else value[0]
                    for key, value in self.md.Meta.items()}

        return html, meta


class JinjaRenderer:
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
        text = env.get_template(template + ".html").render(args)
        with open(outpath, 'w') as outfile:
            outfile.write(text)

if __name__ == "__main__":
    SiteGenerator(DIRS, SITE, MarkdownReader, JinjaRenderer).publish()
