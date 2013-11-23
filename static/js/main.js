// 全局配置
require.config({
    baseUrl: '/static/js',
    paths: {
        bootstrap: 'lib/bootstrap.min',
        jquery: 'lib/jquery-1.10.1.min',
        blog: 'app/blog',
        favsite: 'app/favsite',
    }
});

require(['jquery', 'blog', 'favsite'],
function($, blog, favsite) {
    // 禁用cache
    $.ajaxSetup({
        cache : false
    });

	$(function() {
		blog.init();
		favsite.init();
	});
});
