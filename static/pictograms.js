(function () {
    "use strict";

    $(document).ready(function () {
        var MINIMUM_QUERY_LENGTH = parseInt($("#minimum-query-length").val());
        var $form = $("form");
        var navHeight = $("nav")[0].getBoundingClientRect().bottom;
        var formTop = $form[0].getBoundingClientRect().top - navHeight - 16; // 1 rem padding (16 px)

        var $modal = $("#full-size-image-modal");
        var $modalTitle = $("#image-title");
        var $fullSizeImage = $("#full-size-image");
        $modal.on("show.bs.modal", function (e) {
            var $image = $(e.relatedTarget).find("img");
            var url = $image.attr("data-original");
            var title = $image.attr("alt");
            $modalTitle.text('Pictogram for "' + title + '"');
            $fullSizeImage.attr("alt", title).attr("src", url);
        });

        var $results = $("#results").on("draw.dt", function () {
            $results.find("img").lazyload();
            window.scrollTo(0, formTop);
        });
        var dt = $results.DataTable($.extend(window.DATATABLE_OPTIONS, {
            "columns": [
                null,
                {
                    "data": function (row) {
                        return row[1]; // image urls only
                    },
                    "render": function (data, type, row) {
                        // convert url array to img tags for display
                        if (type === "display") {
                            var r = "";
                            $.each(data, function (_, pictogram_id) {
                                r += '<a href="#" data-toggle="modal" data-target="#full-size-image-modal">';
                                r += '<img width="100" height="100" alt="' + row[0] + '" data-original="' +
                                    Flask.url_for("static_pictogram", {"pictogram_id": pictogram_id}) + '">';
                                r += "</a>";
                            });
                            return r;
                        }
                        return data;
                    }
                }
            ]
        }));

        var $query = $("#query").on("input paste propertychange", function () {
            $query.siblings("button").prop("disabled", $query.val().trim().length < MINIMUM_QUERY_LENGTH);
        });

        $form.submit(function (e) {
            e.preventDefault();
            var params = {
                "query": $query.val().trim(),
                "page": 0
            };

            $results.trigger("preXhr.dt");
            dt.clear().draw();
            var xhrs = [];
            $.get($form.attr("action") + "?" + $.param(params), function (response) {
                dt.rows.add(response.data).draw();
                for (var i = 1; i <= response.maxPages; i++) {
                    // jshint loopfunc: true
                    params.page = i;
                    xhrs.push($.get($form.attr("action") + "?" + $.param(params), function (response) {
                        dt.rows.add(response.data).draw();
                    }));
                }
                $.when.apply(this, xhrs).done(function () {
                    $results.trigger("xhr.dt");
                });
            }).fail(function () {
                $results.trigger("xhr.dt");
            });
        });
    });
}());
