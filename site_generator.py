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
    def __init__(self, dirs, site):
        self.dirs = dirs
        self.site = site

    def publish(self):
        self.render_posts()
        self.render_tags()
        self.render_root()
        self.render_projects()
        self.render_rss()

    def render_posts(self):
        self.posts = []
        for post in listdir(self.dirs['posts']):
            self.posts.append(Post(self.dirs['posts'], post, self.dirs, self.site))
        
        self.posts = sorted(self.posts, key=lambda x: x.date, reverse=True)

        # Populate previous and next post attributes
        for post in self.posts:
            post.set_neighbours(self.posts)

        self.args = {'posts': self.posts}

        for post in self.posts:
            post.render('post.html', self.args, post.link)

        ## Render index
        index_args = self.args
        index_args['index'] = True

        index_post = self.posts[0]
        index_post.render('post.html', index_args, 'index.html')
        
    def render_tags(self):
        makedirs(join(self.dirs['site'], "tag"))

        tag_dict = defaultdict(list)
        for post in self.posts:
            for tag in post.meta.get('tags'):
                tag_dict[tag].append(post)

        for tag, tagged_posts in tag_dict.items():
            page = Page(self.dirs['root'], 'tag.md', self.dirs)
            args = {'posts': self.posts,
                    'tag_posts': tagged_posts,
                    'tag': tag}
            out = join("tag", tag)

            page.render('tag.html', args, out)

    def render_root(self):
        for root_page in listdir(self.dirs['root']):
            page = Page(self.dirs['root'], root_page, self.dirs)
            url = page.meta.get('url')
            if url:   
                page.render(url + '.html', self.args, url)

    def render_projects(self):
        for project in listdir(self.dirs['projects']):
            page = Page(self.dirs['projects'], project, self.dirs)
            out = join(self.dirs['projects'], page.meta.get('url'))
            page.render("project.html", self.args, out)

    def render_rss(self):
        feed = FeedGenerator()
        feed.id(self.site['url'])
        feed.title(self.site['title'])
        feed.author({'name': self.site['name'], 'email': self.site['email']})
        feed.link(href=self.site['url'], rel="self")
        feed.language('en')

        for post in self.posts:
            post.set_rss_attributes(feed)

        feed.atom_file(join(self.dirs['site'], 'rss'), pretty=True)
                    
class Page(object):
    """Base class for static website page rendering"""

    def __init__(self, directory, fname, dirs):
        self.dirs = dirs
        self.path = join(directory, fname)
        self.read_markdown()

    def read_markdown(self):
        md = Markdown(extensions=['markdown.extensions.extra',
                                  'markdown.extensions.meta',
                                  'markdown.extensions.smarty'],
                      output_format='html5')

        with open(self.path, 'r') as f:
            self.html = md.convert(f.read())
            
        self.meta = {key: value if key == "tags" else value[0]
                     for key, value in md.Meta.items()}

    def render(self, template, args, outpath=None):
        """Method for rendering Pages with markdown and jinja2"""

        outpath = join(self.dirs['site'], outpath)

        args['post'] = self
        args['content'] = self.html

        # Create directory if necessary
        if not exists(dirname(outpath)):
            makedirs(dirname(outpath))

        # Use jinja to render template and save
        loader = FileSystemLoader(self.dirs['templates'])
        env = Environment(loader=loader)
        text = env.get_template(template).render(args)
        with open(outpath, 'w') as outfile:
            outfile.write(text)

class Post(Page):
    def __init__(self, directory, fname, dirs, site):
        Page.__init__(self, directory, fname, dirs)

        self.site = site
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

    def set_rss_attributes(self, feed):
        """
        Set RSS atrributes for a post.

        Given a python-feedgenerator object, this adds an entry for
        the post from the post content and metadata.

        """

        feed_entry = feed.add_entry()
        feed_entry.id(join(self.site['url'], self.link))
        feed_entry.title(self.meta.get('title'))
        feed_entry.published(self.date)
        feed_entry.updated(self.meta.get('updated'))

        # Full content with hardlinked images
        content = self.html.replace('src="/' + self.dirs['images'],
                                    'src="{}'.format(join(self.site['url'], self.dirs['images'])))
        feed_entry.content(content, type="html")
    
if __name__ == "__main__":
    generator = SiteGenerator(dirs, site)
    generator.publish()
