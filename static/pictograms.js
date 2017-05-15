"use strict";

$(document).ready(function () {
    $("#results").DataTable($.extend(DATATABLE_OPTIONS, {
        "columns": [
            null,
            {
                "data": function (row) {
                    return row[1]; // image urls only
                },
                "render": function (data, type) {
                    // convert url array to img tags for display
                    if (type === "display") {
                        var r = "";
                        $.each(data, function (i, url) {
                            r += '<img width="100" height="100" src="' + url + '">';
                        });
                        return r;
                    }
                    return data;
                }
            }
        ]
    }));
});
