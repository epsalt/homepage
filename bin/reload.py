import livereload
import re

server = livereload.Server()
dirs = (
    "content",
    "templates",
    "config.yaml",
)


def ignore(f):
    return bool(re.match(r"\.\#.+$", f))


for d in dirs:
    server.watch(d, func="npm run build:content", ignore=ignore)

server.serve()
