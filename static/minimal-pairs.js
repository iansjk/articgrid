(function () {
    $(document).ready(function () {
        $("form").submit(function (e) {
            e.preventDefault();
            var form = $(this);
            var url = form.attr("action");
            $.post(url, form.serialize(), function (data) {
                var results = $("#results").show().find("tbody").empty();
                $.each(data.results, function (i, item) {
                    var row = $("<tr>").appendTo(results);
                    row.append($("<td>").text(item[0]));
                    row.append($("<td>").text(item[1]));
                });
            });
        });
    });
})();
