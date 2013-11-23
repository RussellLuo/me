define(['jquery'],
function($) { 
    // 禁用cache
    $.ajaxSetup({
        cache : false
    });

    return {
        init: function() {
            // 给Markdown文章中的标题添加样式（参考/static/css/style.css中的"target-with-top-navbar"）
            var titleTags = ["h1", "h2", "h3", "h4", "h5", "h6"];
            $.each(titleTags, function(i, d) {
                $("#markdown " + d).addClass("target-with-top-navbar");
            });

            // 为所有h1标题生成链接，进而在侧边栏中用于导航
            var num = 0;
            $.each($("#markdown h1"), function(i, d) {
                var anchor_link = $(d).attr("id");

                /* Judge if element $(d) has [id] attribute
                   thank Domenic, see http://stackoverflow.com/questions/1318076/jquery-hasattr-checking-to-see-if-there-is-an-attribute-on-an-element */
                if (!$(d).is("[id]")) {
                    anchor_link = "sidebar-anchor-link-" + num.toString();
                    $(d).attr("id", anchor_link);
                    num += 1;
                }
                var url = $(location).attr('href');
                var anchor_title = $(d).text();
                $("#blog-post-view li#prev-and-next").prev().after('<li><a href="' + url + "#" + anchor_link + '">' + anchor_title + "</a></li>")
            });

            /* 用"链接<a>"模拟"按钮<button>"：去掉<a>标签的href属性，并修改光标为箭头
               see http://stackoverflow.com/questions/5605481/css-html-disable-link-hover-text,
               and http://stackoverflow.com/questions/1843674/how-to-change-cursor-from-pointer-to-finger-using-jquery */
            $("#do-recommend").removeAttr("href").css("cursor", "pointer");

            // 点击"推荐"
            var url = window.location.href;
            $("#do-recommend").click(function(event) {
                /* Send the data using post */
                $.post(url, {do_recommend: true},
                    function(data) {
                        if (data.status == "ok") {
                            $("#do-recommend").html('<span class="glyphicon glyphicon-thumbs-up"></span> 推荐(' + data.starred.toString() + ')');
                            $("#recommend-status-tip").text("");
                        }
                        else {
                            $("#recommend-status-tip").text("不能重复推荐！");
                        }
                    }, "json");
            });
        }
    }
});
