(function() {
    $(document).ready(function () {
        var results = $("#results");
        var submit = $("button[type=submit]");
        var images_th = results.find('th').last();
        $("form").on("submit", function (e) {
            var form = $(this);
            e.preventDefault();
            submit.text("Working...").prop("disabled", true);
            var query = $("#query").val();
            $.get(form.attr("action"), form.serialize(), function (data) {
                tbody = results.children("tbody").empty();
                $.each(data.results, function (term, images) {
                    var tr = $("<tr>").appendTo(tbody);
                    tr.append($("<td>").text(term));
                    $.each(images, function (i, image) {
                        tr.append($("<td>")
                            .append($("<img>")
                                .attr("width", 100)
                                .attr("height", 100)
                                .attr("src", image)));
                    });
                    images_th.prop("colspan",
                        Math.max(images_th.prop("colspan"), images.length));

                });

                // update colspans of rows now that max number of cells is known
                var max_images = images_th.prop("colspan");
                tbody.children().each(function () {
                    var row = $(this);
                    var num_images = row.children().length - 1;
                    if (num_images === 1) {
                        row.children().last().attr("colspan", max_images);
                    } else {
                        row.children(":not(:first)").each(function (c) {
                            var cell = $(this);
                            var auto_colspan = Math.floor(max_images /
                                num_images);
                            if (c === num_images - 1) {
                                cell.attr("colspan",
                                    max_images - (auto_colspan * (num_images
                                    - 1)));
                            } else {
                                cell.attr("colspan", auto_colspan);
                            }
                        });
                    }
                });
                submit.text("Search").prop("disabled", false);
            });
        });
    });
})();
