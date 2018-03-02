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

POST_DIR = 'posts/'
TEMPLATE_DIR = 'templates'
PROJ_DIR = 'projects'
SITE_DIR = 'site/'
SITE_URL = 'https://epsalt.ca/'
IMAGE_DIR = 'images/'

class Page(object):
    """Base class for static website page rendering"""

    def __init__(self, md_fname):
        md = Markdown(extensions=['markdown.extensions.extra',
                                  'markdown.extensions.meta',
                                  'markdown.extensions.smarty'],
                      output_format='html5')

        with open(md_fname, 'r') as md_file:
            self.html = md.convert(md_file.read())

        # Remove list wrapping from everything except actual lists
        self.meta = {key: value if key == "tags" else value[0]
                     for key, value in md.Meta.items()}

    def render(self, template, template_args, outpath=None):
        """Method for rendering Pages with markdown and jinja2"""

        outpath = join(SITE_DIR, outpath)

        # Build jinja template argument dict
        args = {'post': self,
                'content': self.html}
        for key, value in template_args.items():
            args[key] = value

        # Create directory if necessary
        if not exists(dirname(outpath)):
            makedirs(dirname(outpath))

        # Use jinja to render template and save
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        text = env.get_template(template).render(args)
        with open(outpath, 'w') as outfile:
            outfile.write(text)

class Post(Page):
    """Class for blog posts, extends Page"""

    def __init__(self, f):
        Page.__init__(self, f)

        self.date = parse(self.meta.get('date'))
        self.directory = join(self.date.strftime('%Y'),
                              self.date.strftime('%m'))
        self.link = join(self.directory, self.meta.get('url'))
        self.ppost = None
        self.npost = None

    def set_neighbours(self, posts):
        """
        Sets npost and ppost attributes.

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
        Update RSS atrributes.

        Given a python-feedgenerator object, this adds an entry for
        the post from the post content and metadata.

        """

        # Metadata tags
        feed_entry = feed.add_entry()
        feed_entry.id(join(SITE_URL, self.link))
        feed_entry.title(self.meta.get('title'))
        feed_entry.published(self.date)
        feed_entry.updated(self.meta.get('updated'))

        # Full content with hardlinked images
        content = self.html.replace('src="/'+IMAGE_DIR,
                                    'src="{}'.format(join(SITE_URL, IMAGE_DIR)))
        feed_entry.content(content, type="html")


def build_rss_feed(posts):
    """Create RSS feed from list of posts"""

    feed = FeedGenerator()
    feed.id(SITE_URL)
    feed.title('from the desk of e.p salt')
    feed.author({'name':'E.P Salt', 'email':'evan@epsalt.ca'})
    feed.link(href=SITE_URL, rel="self")
    feed.language('en')

    for post in posts:
        post.set_rss_attributes(feed)

    # Render RSS page
    feed.atom_file(join(SITE_DIR, 'rss'), pretty=True)

def publish():
    """
    Generate all static site pages.

    This function finds all of the following and renders them as
    html in the SITE_DIR:
    - The about.md and archive.md file in the root directory
    - All posts in POST_DIR
    - All post tag files
    """

    # Get blog posts from POST_DIR
    posts = [Post(join(POST_DIR, post)) for post in listdir(POST_DIR)]
    sorted_posts = sorted(posts, key=lambda x: x.date, reverse=True)

    # Add previous and next post attributes to Post Class
    for post in sorted_posts:
        post.set_neighbours(sorted_posts)

    # Jinja2 template arguments
    args = {'posts': sorted_posts}

    # Build tag dict and render tag pages
    makedirs(join(SITE_DIR, "tag"))
    tag_dict = defaultdict(list)
    for post in sorted_posts:
        for tag in post.meta.get('tags'):
            tag_dict[tag].append(post)

    for tag, posts in tag_dict.items():
        out = join("tag", tag)
        tag_args = {'posts': sorted_posts,
                    'tag_posts': posts,
                    'tag': tag}
        Page(join(TEMPLATE_DIR, 'tag.md')).render('tag.html', tag_args, out)

    # Render all blog posts
    for post in sorted_posts:
        post.render('post.html', args, post.link)

    # Render site root pages
    for root in ['about', 'archive', '404']:
        root_page = Page(join(TEMPLATE_DIR, root + '.md'))
        root_page.render(root + '.html', args, root_page.meta.get('url'))

    # Render project pages
    projects = [Page(join(PROJ_DIR, proj)) for proj in listdir(PROJ_DIR)]
    for project in projects:
        project.render("project.html", args, join(PROJ_DIR, project.meta.get('url')))

    # Index page
    index_args = args
    index_args['index'] = True
    sorted_posts[0].render('post.html', index_args, 'index.html')

    build_rss_feed(posts)

if __name__ == "__main__":
    publish()
