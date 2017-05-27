(function () {
    "use strict";

    $(document).ready(function () {
        $("#results").DataTable($.extend(window.DATATABLE_OPTIONS, {
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
                            $.each(data, function (i, pictogram_id) {
                                r += '<img width="100" height="100" src="' +
                                    Flask.url_for("static_pictogram", {"pictogram_id": pictogram_id}) + '">';
                            });
                            return r;
                        }
                        return data;
                    }
                }
            ]
        }));
    });
}());
