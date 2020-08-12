from django.core.management.base import BaseCommand, CommandError
from urllib.parse import urlparse
import requests
import xml.etree.ElementTree as ET
import html
from datetime import datetime
import logging
from ...models import Item, Category


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Grab items from the specified feeds URLs"

    def add_arguments(self, parser):
        parser.add_argument("urls", type=str)

    def handle(self, *args, **kwargs):
        urls = kwargs.get("urls")
        if not urls:
            logger.error("URL should not be empty")
            raise CommandError("URL should not be empty")
        urls = urls.split(",")
        for url in urls:
            try:
                url = urlparse(url).geturl()
                response = requests.get(url)
                root = ET.fromstring(response.content)
                for item in root.findall("./channel/item"):
                    article = Item()
                    for ch in item.getchildren():
                        tag = ch.tag
                        if tag == "category":
                            article.save()
                            categories = ch.text.split("/")
                            for title in categories:
                                category, created = Category.objects.get_or_create(
                                    title=title)
                                if created:
                                    successMessage = (f"Successfully create category "
                                                      f"{category} with URL: {url}")
                                    self.stdout.write(
                                        self.style.SUCCESS(successMessage))
                                    logger.info(successMessage)
                                article.categories.add(category)
                        else:
                            if tag == "description":
                                article.description = html.escape(ch.text)
                            elif tag == "pubDate":
                                article.pub_date = datetime.strptime(
                                    ch.text, "%a, %d %b %Y %H:%M:%S %z")
                            elif tag == "guid":
                                article.guid = int(ch.text)
                            else:
                                setattr(article, tag, ch.text)
                    article.save()
                    self.stdout.write(self.style.SUCCESS(f"{article}"))
                successMessage = f"Successfully grab items with URL: {url}"
                self.stdout.write(self.style.SUCCESS(successMessage))
                logger.info(successMessage)
            except requests.exceptions.MissingSchema:
                error = f"Invalid URL: {url}"
                self.stderr.write(self.style.ERROR(error))
                logger.exception(error)
