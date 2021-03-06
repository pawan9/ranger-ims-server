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
Incident reports page element.
"""

from twisted.web.iweb import IRequest
from twisted.web.template import Tag, renderer

from ims.auth import Authorization
from ims.config import Configuration
from ims.ext.json import jsonFalse, jsonTrue
from ims.ext.klein import KleinRenderable

from .._page import Page
from ..reports_template._reports_template import title


__all__ = ()



class IncidentReportsPage(Page):
    """
    Incident reports page element.
    """

    def __init__(self, config: Configuration) -> None:
        super().__init__(config=config, title=title)


    @renderer
    def editing_allowed(self, request: IRequest, tag: Tag) -> KleinRenderable:
        """
        JSON boolean, true if editing is allowed.
        """
        if (request.authorizations & Authorization.writeIncidentReports):
            return jsonTrue
        else:
            return jsonFalse
