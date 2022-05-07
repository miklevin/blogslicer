# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['index_front_matter', 'journal_path', 'output_path', 'slicer', 'dates', 'counter', 'date_next', 'table',
           'at_top', 'index_list', 'index_page']

# Cell

import argparse
from pathlib import Path
from dateutil import parser
from slugify import slugify
from dumbquotes import dumbquote


if hasattr(__builtins__, "__IPYTHON__") or __name__ != '__main__':
    from IPython.display import display, Markdown

    h1 = lambda text: display(Markdown(f"# {text}"))
    h2 = lambda text: display(Markdown(f"## {text}"))
    h3 = lambda text: display(Markdown(f"### {text}"))

    folder_name = "../pythonically"
    blog_title = "Pythonic Ally Blog"
    blog_slug = "blog"
    author = "Mike Levin"
else:
    h1 = lambda text: print(f"# {text}")
    h2 = lambda text: print(f"## {text}")
    h3 = lambda text: print(f"## {text}")

    aparser = argparse.ArgumentParser()
    add_arg = aparser.add_argument
    add_arg("-p", "--path", required=True)
    add_arg("-t", "--title", required=True)
    add_arg("-s", "--slug", required=True)
    add_arg("-a", "--author", required=True)
    args = aparser.parse_args()

    folder_name = args.path
    blog_title = args.title
    blog_slug = args.slug
    author = args.author

index_front_matter = f"""---
layout: default
author: {author}
title: "{blog_title}"
slug: {blog_slug}
permalink: /blog/
---
"""

# [{blog_title} as 1 page](/journal/)


journal_path = f"{folder_name}/journal.md"
output_path = f"{folder_name}/_posts/"
slicer = "-" * 80

Path(output_path).mkdir(exist_ok=True)

dates = []
counter = -1
date_next = False
with open(journal_path, "r") as fh:
    for line in fh:
        line = line.rstrip()
        if date_next:
            try:
                adate = line[3:]
                date_next = False
                adatetime = parser.parse(adate).date()
            except:
                adatetime = None
            dates.append(adatetime)
            date_next = False
        if line == slicer:
            date_next = True
            counter = counter + 1
dates.reverse()

table = []
at_top = True
index_list = []
with open(journal_path, "r") as fh:
    for i, line in enumerate(fh):
        line = line.rstrip()
        if line == slicer:
            if at_top:
                at_top = False
                table = []
                continue
            adatetime = dates[counter - 1]
            filename = f"{output_path}{adatetime}-post-{counter}.md"
            h3(f"FILE: {filename}")
            with open(filename, "w") as fw:
                title = f"Post {counter}"
                slug = title
                if table[0] == slicer:
                    table = table[1:]
                maybe = table[1]
                has_title = False
                if table and maybe and maybe[0] == "#":
                    title = maybe[maybe.find(" ") + 1 :]
                    has_title = True
                slug = title.replace("'", "")
                slug = slugify(slug)
                top = []
                top.append("---\n")
                top.append("layout: post\n")
                top.append(f'title: "{title}"\n')
                top.append(f'author: "{author}"\n')
                top.append(f"categories: {blog_slug}\n")
                top.append(f"slug: {slug}\n")
                top.append(f"permalink: /{blog_slug}/{slug}/\n")
                link = f"- [{title}](/{blog_slug}/{slug}/) {adatetime}"
                index_list.append(link)
                top.append("---\n")
                top.append("\n")
                top_chop = 2
                if has_title:
                    top_chop = 3
                table = [f"{x}\n" for x in table[top_chop:]]
                table = top + table
                print("".join(table))
                fw.writelines(table)
            counter = counter - 1
            table = []
        table.append(line)

index_page = index_front_matter + "\n\n" + "\n".join(index_list)

with open(f"{folder_name}/blog.md", "w") as fh:
    fh.writelines(index_page)