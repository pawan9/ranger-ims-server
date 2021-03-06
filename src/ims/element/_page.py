##
# See the file COPYRIGHT for copyright information.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

"""
Element base classes.
"""

from twisted.web.iweb import IRequest
from twisted.web.template import Tag, renderer, tags

from ims.config import Configuration
from ims.ext.klein import KleinRenderable

from ._element import Element
from .footer import FooterElement
from .header import HeaderElement
from .nav import NavElement


__all__ = ()



class Page(Element):
    """
    XHTML page element.
    """

    def __init__(self, config: Configuration, title: str) -> None:
        super().__init__(config=config)
        self.titleText = title


    @renderer
    def title(
        self, request: IRequest, tag: Tag = tags.title
    ) -> KleinRenderable:
        """
        `<title>` element.
        """
        if self.titleText is None:
            titleText = ""
        else:
            titleText = self.titleText

        return tag(titleText)


    @renderer
    def head(self, request: IRequest, tag: Tag = tags.head) -> KleinRenderable:
        """
        <head> element.
        """
        urls = self.config.urls

        children = tag.children
        tag.children = []

        return tag(
            tags.meta(charset="utf-8"),
            tags.meta(
                name="viewport", content="width=device-width, initial-scale=1"
            ),
            tags.link(
                type="image/png", rel="icon",
                href=urls.logo.asText(),
            ),
            tags.link(
                type="text/css", rel="stylesheet", media="screen",
                href=urls.bootstrapCSS.asText(),
            ),
            tags.link(
                type="text/css", rel="stylesheet", media="screen",
                href=urls.styleSheet.asText(),
            ),
            tags.script(src=urls.jqueryJS.asText()),
            tags.script(src=urls.bootstrapJS.asText()),
            self.title(request),
            children,
        )


    @renderer
    def container(self, request: IRequest, tag: Tag) -> KleinRenderable:
        """
        App container.
        """
        tag.children.insert(0, self.top(request))
        return tag(self.bottom(request), Class="container-fluid")


    @renderer
    def top(self, request: IRequest, tag: Tag = tags.div) -> KleinRenderable:
        """
        Top elements.
        """
        return (
            self.nav(request),
            self.header(request),
            self.title(request, tags.h1),
        )


    @renderer
    def bottom(
        self, request: IRequest, tag: Tag = tags.div
    ) -> KleinRenderable:
        """
        Bottom elements.
        """
        return (self.footer(request),)


    @renderer
    def nav(self, request: IRequest, tag: Tag = tags.nav) -> KleinRenderable:
        """
        <nav> element.
        """
        return NavElement(config=self.config)


    @renderer
    def header(
        self, request: IRequest, tag: Tag = tags.header
    ) -> KleinRenderable:
        """
        <header> element.
        """
        return HeaderElement(config=self.config)


    @renderer
    def footer(
        self, request: IRequest, tag: Tag = tags.footer
    ) -> KleinRenderable:
        """
        <footer> element.
        """
        return FooterElement(config=self.config)
