/**
 * Created by YAN on 2017/4/22.
 */
function set_brand_list(cat, platform) {
    $.getJSON("../get_brand/", {"cat": cat, "platform": platform}, function (data) {
        var tpl = "<li class='brand'><a href='#'>{{= it.brand }}</a></li>";
        var evalText = doT.template(tpl);
        var brand_ul = $("#brand_ul");
        var content = "";
        $.each(data, function (i, item) {
            content += evalText(item.fields)
        });
        brand_ul.html(content);
        init_brand_click();
    })
}

function init_brand_click() {
    $(".brand").each(function () {
        $(this).click(function () {
            var brand = $(this).text(),
                cat = $("#show_cat").text(),
                platform = $("#show_platform").text();
            $("#show_brand").text(brand)
        })
    });
    $(".brand").first().click()
}

function init_cat_click() {
    $(".cat").each(function () {
        $(this).click(function () {
            var cat = $(this).text(),
                platform = $("#show_platform").text();
            $("#show_cat").text(cat);
            if(cat && platform)
            {
                set_brand_list(cat, platform);
            }
        })
    });
    $(".cat").first().click()
}

function init_platform_click() {
    $(".platform").each(function () {
        $(this).click(function () {
            var platform = $(this).text(),
                cat = $("#show_cat").text();
            $("#show_platform").text(platform);
            if(cat && platform)
            {
                set_brand_list(cat, platform);
            }
        })
    });
    $(".platform").first().click()
}

function init_confirm_click() {
    $("#confirm").click(function () {
        $(this).text("采集中");
        $(this).attr("disabled", true);
        var platform = $("#show_platform").text(),
            brand = $("#show_brand").text(),
            cat = $("#show_cat").text();
        $.getJSON("../crawl_comment",{'platform':platform, 'cat':cat, 'brand':brand},function (data) {
            $("#confirm").text("确定");
            $("#confirm").attr("disabled", false);
            alert(data['output_file'])
        })
    })
}

function init_download_click() {
    $("#download").click(function () {
        var platform = $("#show_platform").text(),
            brand = $("#show_brand").text(),
            cat = $("#show_cat").text();
        window.frames["d_iframe"].location.href= "../download/?platform="+platform+"&brand="+brand+"&cat="+cat;
        function sa() {
            if(window.frames["d_iframe"].document.readyState!=="complete")
                setTimeout("sa()",   100);
            else
            window.frames["d_iframe"].document.execCommand('SaveAs');
        }
        sa()
    });
}

function init_click() {
    init_brand_click();
    init_cat_click();
    init_platform_click();
    init_confirm_click();
    init_download_click();
}