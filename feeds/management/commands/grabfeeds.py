from django.core.management.base import BaseCommand, CommandError
from urllib.parse import urlparse
import requests
import xml.etree.ElementTree as ET
import html
from datetime import datetime
from typing import List


class Item(object):

    def __init__(self, title: str = "", description: str = "",
                 link: str = "", categories: List[str] = [],
                 comments: str = "", pubDate: str = "", guid: int = 0):
        self.title = title
        self.description = description
        self.link = link
        self.categories = categories
        self.comments = comments
        self.pubDate = pubDate
        self.guid = guid

    def __repr__(self):
        guid = categories = ""
        if self.guid:
            guid = str(self.guid)
        if self.categories:
            categories = "\n\t+ "\
                .join(category for category in self.categories)
            categories = f"\n\t+ {categories}"
        return (f"Article:\n"
                f"- Title: {self.title}\n"
                f"- Description: {self.description}\n"
                f"- Link: {self.link}\n"
                f"- Categories: {categories}\n"
                f"- Comments: {self.comments}\n"
                f"- Published Date: {self.pubDate}\n"
                f"- GUID: {guid}\n")


class Command(BaseCommand):
    help = "Grab items from the specified feeds URLs"

    def add_arguments(self, parser):
        parser.add_argument("urls", type=str)

    def handle(self, *args, **kwargs):
        urls = kwargs.get("urls")
        if not urls:
            raise CommandError("URL should not be empty")
        urls = urls.split(",")
        for url in urls:
            articles = []
            try:
                url = urlparse(url).geturl()
                response = requests.get(url)
                root = ET.fromstring(response.content)
                for item in root.findall("./channel/item"):
                    article = Item()
                    for ch in item.getchildren():
                        if ch.tag == "category":
                            categories = ch.text.split("/")
                            setattr(article, "categories", categories)
                        else:
                            attribute = ch.text
                            if ch.tag == "description":
                                attribute = html.escape(ch.text)
                            elif ch.tag == "pubDate":
                                attribute = datetime.strptime(
                                    attribute, "%a, %d %b %Y %H:%M:%S %z")
                            elif ch.tag == "guid":
                                attribute = int(attribute)
                            setattr(article, ch.tag, attribute)
                    articles.append(article)
                self.stdout.write(self.style.SUCCESS(
                    f"Successfully grab items with URL: {url}"))
                for article in articles:
                    self.stdout.write(self.style.SUCCESS(
                        f"{article}"))
            except requests.exceptions.MissingSchema:
                self.stderr.write(self.style.ERROR(
                    f"Invalid URL {url}"))
