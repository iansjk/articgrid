(function () {
    "use strict";

    $(document).ready(function () {
        var MINIMUM_QUERY_LENGTH = parseInt($("#minimum-query-length").val());
        var $results = $("#results");
        var dt = $results.DataTable($.extend(window.DATATABLE_OPTIONS, {
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


        var $query = $("#query").on("input paste propertychange", function() {
            $query.siblings("button").prop("disabled", $query.val().trim().length < MINIMUM_QUERY_LENGTH);
        });

        var $form = $("form");
        $form.submit(function(e) {
            e.preventDefault();
            var params = {
                "query": $query.val().trim(),
                "page": 0
            };

            $results.trigger("preXhr.dt");
            var xhrs = [];
            $.get($form.attr("action") + "?" + $.param(params), function(response) {
                dt.rows.add(response.data).draw();
                for (var i = 1; i <= response.maxPages; i++) {
                    // jshint loopfunc: true
                    params.page = i;
                    xhrs.push($.get($form.attr("action") + "?" + $.param(params), function(response) {
                        dt.rows.add(response.data).draw();
                    }));
                }
                $.when.apply(this, xhrs).done(function() {
                    $results.trigger("xhr.dt");
                });
            }).fail(function() {
                $results.trigger("xhr.dt");
            });
        });
    });
}());
