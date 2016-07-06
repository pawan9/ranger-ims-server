// See the file COPYRIGHT for copyright information.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.



//
// Initialize UI
//

function initIncidentReportPage() {
    function loadedIncidentReport() {
    }

    function loadedBody() {
        disableEditing();
        loadAndDisplayIncidentReport(loadedIncidentReport);
    }

    loadBody(loadedBody);
}


//
// Load incident report
//

var incidentReport = null;

function loadIncidentReport(success) {
    var number = null;
    if (incidentReport == null) {
        // First time here.  Use page JavaScript initial value.
        number = incidentReportNumber;
    } else {
        // We have an incident already.  Use that number.
        number = incidentReport.number;
    }

    function ok(data, status, xhr) {
        incidentReport = data;

        if (success != undefined) {
            success();
        }
    }

    function fail(error, status, xhr) {
        disableEditing();
        var message = "Failed to load incident report:\n" + error;
        console.error(message);
        window.alert(message);
    }

    if (number == null) {
        ok({
            "number": null,
            "created": null,
        });
    } else {
        var url = incidentReportsURL + "/" + number;
        jsonRequest(url, null, ok, fail);
    }
}


function loadAndDisplayIncidentReport(success) {
    function loaded() {
        if (incidentReport == null) {
            var message = "Incident report failed to load";
            console.log(message);
            alert(message);
            return;
        }

        drawReportEntries(incidentReport.report_entries);
        $("#incident_report_add").on("input", reportEntryEdited);

        if (editingAllowed) {
            enableEditing();
        }

        if (success != undefined) {
            success();
        }
    }

    loadIncidentReport(loaded);
}


//
// Editing
//

function sendEdits(edits, success, error) {
    var number = incidentReport.number
    var url = incidentReportsURL + "/";

    if (number == null) {
        // We're creating a new incident report.
        var required = [];
        for (var i in required) {
            var key = required[i];
            if (edits[key] == undefined) {
                edits[key] = incidentReport[key];
            }
        }
    } else {
        // We're editing an existing incident report.
        edits.number = number;
        url += number;
    }

    function ok(data, status, xhr) {
        if (number == null) {
            // We created a new incident report.
            // We need to find out the create incident report number so that
            // future edits don't keep creating new resources.

            newNumber = xhr.getResponseHeader("Incident-Report-Number")
            // Check that we got a value back
            if (newNumber == null) {
                fail("No Incident-Report-Number header provided.", status, xhr);
                return;
            }

            newNumber = parseInt(newNumber);
            // Check that the value we got back is valid
            if (isNaN(newNumber)) {
                fail(
                    "Non-integer Incident-Report-Number header provided:" +
                    newNumber,
                    status, xhr
                );
                return;
            }

            // Store the new number in our incident object
            incidentReport.number = newNumber;
        }

        success();
        loadAndDisplayIncidentReport();
    }

    function fail(requestError, status, xhr) {
        var message = "Failed to apply edit:\n" + requestError
        console.log(message);
        error();
        loadAndDisplayIncidentReport();
        window.alert(message);
    }

    jsonRequest(url, edits, ok, fail);
}
