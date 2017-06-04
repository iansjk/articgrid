(function () {
    "use strict";

    var wordbank = {};
    var $wordbank = $("#wordbank");

    function removeWord(word) {
        $wordbank.find("li").filter(function () {
            return $(this).find(".word").text().trim() === word;
        }).remove();
        delete wordbank[word];
    }

    $(document).ready(function () {
        var $prototype = $("#prototype");
        $("#results").on("select.dt deselect.dt", function (e, dt, __, indexes) {
            var words = dt.rows(indexes).data().pop();
            for (var i = 0; i < words.length; i++) {
                if (e.type === "select" && !wordbank[words[i]]) {
                    $prototype.clone().removeAttr("id").show().appendTo($wordbank).find(".word").text(words[i]);
                    wordbank[words[i]] = true;
                } else if (e.type === "deselect") {
                    removeWord(words[i]);
                }
            }
        });

        $wordbank.on("click", ".close", function () {
            removeWord($(this).siblings(".word").text());
        });
    });
})();
