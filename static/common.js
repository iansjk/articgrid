(function () {
    "use strict";

    $.fn.dataTable.ext.errMode = "throw";

    window.DATATABLE_OPTIONS = {
        "language": {"emptyTable": "No results to display."}
    };

    $(document).ready(function () {
        $("#results").not('[data-defer-init="true"]').DataTable(window.DATATABLE_OPTIONS);
        $("form[action]").submit(function (e) {
            e.preventDefault();
            var $form = $(this);
            var url = $form.attr("action");
            var $submit = $form.find('button[type="submit"]');
            var origText = $submit.text();
            $submit.width($submit.width()).html('<i class="fa fa-circle-o-notch fa-spin"></i><span class="sr-only">Loading...</span>').prop("disabled", true);
            $("#results").DataTable().on("xhr.dt", function (_, __, ___, xhr) {
                xhr.always(function () {
                    $submit.prop("disabled", false).text(origText);
                });
            }).ajax.url(url + "?" + $form.serialize()).load();
        });
    });
}());
