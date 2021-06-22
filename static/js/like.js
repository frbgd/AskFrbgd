function send_like(aLink, mark) {
    console.log(aLink);
    console.log(mark);

    var questionId = aLink.attr("questionId");

    $.ajax({
        url : "/question/" + questionId + "/like/",
        type : "POST",
        data: JSON.stringify({'mark': mark}),
        dataType: 'json',

        success : function(json) {
            console.log(json);

            if (json.mark === mark) {
                aLink.removeAttr("href");
            }
            if (mark === 1) {
                $('a[id=' + questionId + '-dislike]').attr("href", "#" + questionId + "-row");
            } else if (mark === -1) {
                $('a[id=' + questionId + '-like]').attr("href", "#" + questionId + "-row");
            }

            var countSpan = $('span[id=' + questionId + '-likeCount]');
            var count = parseInt(countSpan.text());
            countSpan.text(count + mark);

            console.log("success");
        },

        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

$('a[name=like]').click(function() {
    if ($(this).attr("href")) {
        send_like($(this), 1);
    }
});
$('a[name=dislike]').click(function() {
    if ($(this).attr("href")) {
        send_like($(this), -1);
    }
});