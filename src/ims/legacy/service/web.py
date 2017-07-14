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
Incident Management System web interface.
"""

from typing import Optional

from twisted.web.iweb import IRequest

from ims.application._auth import AuthProvider, Authorization
from ims.application._klein import notFoundResponse, redirect, router
from ims.application._static import builtInResource, javaScript, styleSheet
from ims.application._urls import URLs
from ims.ext.klein import ContentType, HeaderName, KleinRenderable, static
from ims.model import Event

from ..element.admin import AdminPage
from ..element.admin_acl import AdminAccessControlPage
from ..element.admin_streets import AdminStreetsPage
from ..element.admin_types import AdminIncidentTypesPage
from ..element.incident import IncidentPage
from ..element.incident_template import IncidentTemplatePage
from ..element.queue import DispatchQueuePage
from ..element.queue_template import DispatchQueueTemplatePage
from ..element.report import IncidentReportPage
from ..element.report_template import IncidentReportTemplatePage
from ..element.root import RootPage

Optional  # silence linter


__all__ = (
    "WebMixIn",
)



class WebMixIn(object):
    """
    Mix-in for web interface.
    """

    auth: AuthProvider

    #
    # Static content
    #

    @router.route(URLs.styleSheet, methods=("HEAD", "GET"))
    @static
    def styleSheetResource(self, request: IRequest) -> KleinRenderable:
        """
        Endpoint for global style sheet.
        """
        return styleSheet(request, "style.css")


    @router.route(URLs.logo, methods=("HEAD", "GET"))
    @static
    def logoResource(self, request: IRequest) -> KleinRenderable:
        """
        Endpoint for logo.
        """
        request.setHeader(HeaderName.contentType.value, ContentType.png.value)
        return builtInResource(request, "logo.png")


    @router.route(URLs.imsJS, methods=("HEAD", "GET"))
    @static
    def imsJSResource(self, request: IRequest) -> KleinRenderable:
        """
        Endpoint for C{ims.js}.
        """
        return javaScript(request, "ims.js")


    #
    # Web interface
    #

    @router.route(URLs.root, methods=("HEAD", "GET"))
    def rootResource(self, request: IRequest) -> KleinRenderable:
        """
        Server root page.

        This redirects to the application root page.
        """
        return redirect(request, URLs.prefix)


    @router.route(URLs.prefix, methods=("HEAD", "GET"))
    @static
    def applicationRootResource(self, request: IRequest) -> KleinRenderable:
        """
        Application root page.
        """
        return RootPage(self)


    @router.route(URLs.viewEvent, methods=("HEAD", "GET"))
    def viewEventResource(
        self, request: IRequest, eventID: str
    ) -> KleinRenderable:
        """
        Event root page.

        This redirects to the event's dispatch queue page.
        """
        return redirect(request, URLs.viewDispatchQueueRelative)


    @router.route(URLs.admin, methods=("HEAD", "GET"))
    @static
    async def adminPage(self, request: IRequest) -> KleinRenderable:
        """
        Endpoint for admin page.
        """
        # FIXME: Not strictly required because the underlying data is
        # protected.
        # But the error you get is stupid, so let's avoid that for now.
        await self.auth.authorizeRequest(request, None, Authorization.imsAdmin)
        return AdminPage(self)


    @router.route(URLs.adminJS, methods=("HEAD", "GET"))
    @static
    def adminJSResource(self, request: IRequest) -> KleinRenderable:
        """
        Endpoint for C{admin.js}.
        """
        return javaScript(request, "admin.js")

    @router.route(URLs.adminAccessControl, methods=("HEAD", "GET"))
    async def adminAccessControlPage(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for access control page.
        """
        # FIXME: Not strictly required because the underlying data is
        # protected.
        # But the error you get is stupid, so let's avoid that for now.
        await self.auth.authorizeRequest(request, None, Authorization.imsAdmin)
        return AdminAccessControlPage(self)


    @router.route(URLs.adminAccessControlJS, methods=("HEAD", "GET"))
    @static
    def adminAccessControlJSResource(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for C{admin_acl.js}.
        """
        return javaScript(request, "admin_acl.js")


    @router.route(URLs.adminIncidentTypes, methods=("HEAD", "GET"))
    async def adminAdminIncidentTypesPagePage(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for incident types admin page.
        """
        # FIXME: Not strictly required because the underlying data is
        # protected.
        # But the error you get is stupid, so let's avoid that for now.
        await self.auth.authorizeRequest(request, None, Authorization.imsAdmin)
        return AdminIncidentTypesPage(self)


    @router.route(URLs.adminIncidentTypesJS, methods=("HEAD", "GET"))
    @static
    def adminAdminIncidentTypesPageJSResource(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for C{admin_types.js}.
        """
        return javaScript(request, "admin_types.js")


    @router.route(URLs.adminStreets, methods=("HEAD", "GET"))
    async def adminStreetsPage(self, request: IRequest) -> KleinRenderable:
        """
        Endpoint for streets admin page.
        """
        # FIXME: Not strictly required because the underlying data is
        # protected.
        # But the error you get is stupid, so let's avoid that for now.
        await self.auth.authorizeRequest(request, None, Authorization.imsAdmin)
        return AdminStreetsPage(self)


    @router.route(URLs.adminStreetsJS, methods=("HEAD", "GET"))
    @static
    def adminStreetsJSResource(self, request: IRequest) -> KleinRenderable:
        """
        Endpoint for C{admin_streets.js}.
        """
        return javaScript(request, "admin_streets.js")


    @router.route(URLs.viewDispatchQueue, methods=("HEAD", "GET"))
    async def viewDispatchQueuePage(
        self, request: IRequest, eventID: str
    ) -> KleinRenderable:
        """
        Endpoint for the dispatch queue page.
        """
        event = Event(eventID)
        # FIXME: Not strictly required because the underlying data is
        # protected.
        # But the error you get is stupid, so let's avoid that for now.
        await self.auth.authorizeRequest(
            request, event, Authorization.readIncidents
        )
        return DispatchQueuePage(self, event)


    @router.route(URLs.viewDispatchQueueTemplate, methods=("HEAD", "GET"))
    @static
    def viewDispatchQueueTemplatePage(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for the dispatch queue page template.
        """
        return DispatchQueueTemplatePage(self)


    @router.route(URLs.viewDispatchQueueJS, methods=("HEAD", "GET"))
    @static
    def viewDispatchQueueJSResource(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for C{queue.js}.
        """
        return javaScript(request, "queue.js")


    @router.route(URLs.viewIncidentNumber, methods=("HEAD", "GET"))
    async def viewIncidentPage(
        self, request: IRequest, eventID: str, number: str
    ) -> KleinRenderable:
        """
        Endpoint for the incident page.
        """
        event = Event(eventID)

        numberValue: Optional[int]
        if number == "new":
            authz = Authorization.writeIncidents
            numberValue = None
        else:
            authz = Authorization.readIncidents
            try:
                numberValue = int(number)
            except ValueError:
                return notFoundResponse(request)

        await self.auth.authorizeRequest(request, event, authz)

        return IncidentPage(self, event, numberValue)


    @router.route(URLs.viewIncidentNumberTemplate, methods=("HEAD", "GET"))
    @static
    def viewIncidentNumberTemplatePage(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for the incident page template.
        """
        return IncidentTemplatePage(self)


    @router.route(URLs.viewIncidentNumberJS, methods=("HEAD", "GET"))
    @static
    def incidentJSResource(self, request: IRequest) -> KleinRenderable:
        """
        Endpoint for C{incident.js}.
        """
        return javaScript(request, "incident.js")


    # FIXME: viewIncidentReports


    @router.route(URLs.viewIncidentReport, methods=("HEAD", "GET"))
    async def viewIncidentReportPage(
        self, request: IRequest, number: str
    ) -> KleinRenderable:
        """
        Endpoint for the report page.
        """
        numberValue: Optional[int]
        if number == "new":
            await self.auth.authorizeRequest(
                request, None, Authorization.writeIncidentReports
            )
            numberValue = None
        else:
            try:
                numberValue = int(number)
            except ValueError:
                return notFoundResponse(request)

            await self.auth.authorizeRequestForIncidentReport(
                request, numberValue
            )

        return IncidentReportPage(self, numberValue)


    @router.route(URLs.viewIncidentReportTemplate, methods=("HEAD", "GET"))
    @static
    def viewIncidentReportTemplatePage(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for the incident page template.
        """
        return IncidentReportTemplatePage(self)


    @router.route(URLs.viewIncidentReportJS, methods=("HEAD", "GET"))
    @static
    def viewIncidentReportJSResource(
        self, request: IRequest
    ) -> KleinRenderable:
        """
        Endpoint for C{report.js}.
        """
        return javaScript(request, "report.js")
