(function() {
    $(document).ready(function() {
        $("form").submit(function(e) {
            e.preventDefault();
            var form = $(this);
            $.get(form.attr("action"), form.serialize(), function(data) {
                var results = $("#results").find("tbody").empty();
                $.each(data.results, function(i, word) {
                    var tr = $("<tr>").appendTo(results);
                    tr.append($("<td>").text(word));
                });
            });
        });
    });
})();
