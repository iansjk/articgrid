"use strict";

$.fn.dataTable.ext.errorMode = "throw";

var DATATABLE_OPTIONS = {
    "language": {"emptyTable": "No results to display."}
};

$(document).ready(function () {
    $("#results").not('[data-defer-init="true"]').DataTable(DATATABLE_OPTIONS);
    $("form[action]").submit(function (e) {
        e.preventDefault();
        var $form = $(this);
        var url = $form.attr("action");
        var $submit = $form.find('button[type="submit"]').prop("disabled", true).text("Working...");
        $("#results").DataTable().ajax.url(url + "?" + $form.serialize()).load(function () {
            $submit.prop("disabled", false).text("Search");
        });
    })
});
