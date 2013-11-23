define(['jquery'],
function($) { 
    // 禁用cache
    $.ajaxSetup({
        cache : false
    });

    return {
        init: function() {
            // 进入"爱逛"页面，默认由搜索框获取焦点
            $("#search-togo-input").focus();

            // 从URL中提取主机名
            function getHostname(url) {
                // 匹配URL（http或https），提取其中的主机名（去掉可能的www前缀和多余的后缀）
                var re_hostname = /^https?:\/\/(www\.)?(\w+).*$/;
                var res = url.match(re_hostname);
                if (res == null) {
                    return "";
                }
                else {
                    return res[2];
                }
            }

            // 用于记录当前"缩略图对象"
            var $curThumb = null;

            // "缩略图"处理mouseenter事件，显示"面板"
            function showPanelWhenMouseEnter() {
                $("a.thumbnail").mouseenter(function() {
                    /* get position of the current thumbnail (position = {left: xx, top: xx})
                       see http://stackoverflow.com/questions/683339/how-do-i-find-the-absolute-position-of-an-element-using-jquery
                       and http://stackoverflow.com/questions/3714628/jquery-get-the-location-of-an-element-relative-to-window
                    */
                    var position = $(this).offset();

                    // 与缩略图显示在同一个位置
                    $("#panel-over-thumb").css({
                        left: position.left,
                        top: position.top - $(window).scrollTop(),
                        width: $(this).width() + 10
                    });
                    $("#panel-over-thumb").show();

                    // 记录当前"缩略图对象"
                    $curThumb = $(this);
                });
            }

            // "面板"处理mouseleave事件，隐藏自己
            $("#panel-over-thumb").mouseleave(function() {
                $(this).hide();
            });

            $("#search-togo-form").submit(function(event) {
                // 根据输入文本，匹配网站名称
                var $hit = false;
                var $key = $("#search-togo-input").val();

                $.each($("a.thumbnail"), function(index, value) {
                    $hostname = getHostname($(value).attr("href"));

                    // 字符串统一转换为小写
                    $sitename = $(value).attr("title").toLowerCase();
                    $hostname = $hostname.toLowerCase();
                    $key = $key.toLowerCase();

                    // 如果$sitename或$hostname中包含$key，则匹配命中
                    if ($sitename.indexOf($key) >= 0 || $hostname.indexOf($key) >= 0) {
                        //alert($sitename + "|" + $hostname + "|" + $key);
                        $hit = true;
                        $("#search-togo-input").select(); // 选中文本
                        $(value)[0].click(); // 点击链接
                        return false; // 跳出$.each循环
                    }
                });

                // 匹配未命中
                if (!$hit) {
                    alert("找不到！请试试其他网站吧:-)");
                    $("#search-togo-input").select(); // 选中文本
                }

                // 阻止默认行为
                event.preventDefault();
            });


            // 点击添加网站
            $("#add-site").click(function(event) {
                loadPopupBox();
                resetPopupBox();
            });

            // 点击关闭
            $("#popup-box-close").click(function(event) {
                unloadPopupBox();
            });

            // 显示弹出表单
            function loadPopupBox() { // To Load the Popupbox
                $('#popup-box').fadeIn("slow");
                $("#container").css({ // this is just for style
                    "opacity": "0.3"
                });
            }

            // 恢复弹出表单中控件的状态
            function resetPopupBox() {
                $("#site-name").focus().val("");
                $("#site-name-tip").text("*（必填）").removeClass("warning-text");

                $("#site-url").val("");
                $("#site-url-tip").text("*（必填）").removeClass("warning-text");

                $("#submit-status-tip").text("");
            }

            // 隐藏弹出表单
            function unloadPopupBox() { // TO Unload the Popupbox
                $('#popup-box').fadeOut("slow");
                $("#container").css({ // this is just for style       
                    "opacity": "1" 
                });
            }

            // 表单
            var url = window.location.href;
            $("#popup-form").submit(function(event) {
                // 阻止默认行为
                event.preventDefault();

                /* 名称不能为空 */
                var sitename = $("#site-name").val();
                if (sitename == "") {
                    $("#site-name-tip").addClass("warning-text");
                    return;
                }
                else {
                    $("#site-name-tip").removeClass("warning-text");
                }

                /* 网址必须有效 */
                var siteurl = $("#site-url").val();
                var hostname = getHostname(siteurl);
                if (siteurl == "") {
                    $("#site-url-tip").addClass("warning-text");
                    return;
                }
                else if (hostname == "") {
                    $("#site-url-tip").text("*（无效）").addClass("warning-text");
                    return;
                }
                else {
                    $("#site-url-tip").removeClass("warning-text");
                }

                // 去使能提交按钮，等待本次提交完成
                $("#submit-to-add").attr("disabled", true);
                $("#submit-status-tip").text("正在处理中...").removeClass("ok-text").removeClass("warning-text");

                /* Send the data using post */
                $.post(url, {action: "add", sitename: sitename, siteurl: siteurl},
                    function(data) {
                        if (data == "ok") {
                            $("#site-thumb-grid").append('<div class="c4"><a class="thumbnail" href="' + siteurl + '" title="' + sitename + '" target="_bank"><img src="/static/img/favsite/' + sitename + '.jpg" alt="' + sitename + '" width=256 /></a></div>');
        
                            // 为新增的缩略图绑mouseenter事件
                            showPanelWhenMouseEnter();
        
                            // 复位各控件的状态
                            resetPopupBox();

                            $("#submit-status-tip").text("添加成功").addClass("ok-text");
                        }
                        else if (data == "repeated") {
                            $("#submit-status-tip").text("网站已存在").addClass("warning-text");
                        }
                        else {
                            $("#submit-status-tip").text("添加失败").addClass("warning-text");
                        }

                        // 恢复使能提交按钮
                        $("#submit-to-add").attr("disabled", false);

                    }, "json");
            });

            // 移除缩略图
            $("#thumb-remove-btn").click(function() {
                var sitename = $curThumb.attr("title");
                /* Send the data using post */
                $.post(url, {action: "remove", sitename: sitename},
                    function(data) {
                        if (data == "ok") {
                            $curThumb.closest("div.c4").remove();
                        }
                    }, "json");
            });
        
            // 为当前页面中的缩略图绑定mouseenter事件
            showPanelWhenMouseEnter();
        }
    }
});
