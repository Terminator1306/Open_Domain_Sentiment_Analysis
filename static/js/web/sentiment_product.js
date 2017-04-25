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

function set_product_list(cat, platform, brand) {
    $.getJSON("../get_product", {'cat': cat, 'platform': platform, 'brand': brand},function (data) {
        var tpl = "<li class='product' p_id='{{= it.product_id}}'><a href='#'>{{= it.name }}</a></li>",
            evalText = doT.template(tpl),
            content = "";
        $.each(data, function (i, item) {
            content += evalText(item.fields)
        });
        $("#product_ul").html(content);
        init_product_click();
    });
}

function init_product_click() {
    $(".product").each(function () {
        var product = $(this).text();
        $("#show_product").text(product);
    });
    $(".product").first().click()
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

function init_brand_click() {
    $(".brand").each(function () {
        $(this).click(function () {
            var brand = $(this).text(),
                cat = $("#show_cat").text(),
                platform = $("#show_platform").text();
            set_product_list(cat, platform, brand);
            $("#show_brand").text(brand)
        })
    });
    $(".brand").first().click()
}

function init_click() {
    init_cat_click();
    init_platform_click();
    init_brand_click();
}