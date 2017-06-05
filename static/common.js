(function () {
    "use strict";

    $.fn.dataTable.ext.errMode = "throw";

    window.DATATABLE_OPTIONS = {
        "language": {"emptyTable": "No results to display."}
    };

    $(document).ready(function () {
        var $submit = $("form").find('button[type="submit"]');
        var origText = $submit.text();
        $("#results").on("preXhr.dt", function () {
            $submit.width($submit.width()).html('<i class="fa fa-circle-o-notch fa-spin"></i><span class="sr-only">Loading...</span>').prop("disabled", true);
        }).on("xhr.dt", function () {
            $submit.prop("disabled", false).text(origText);
        });
    });
}());
