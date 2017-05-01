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
        var tpl = "<li class='product' p_id='{{= it.pk}}'><a href='#'>{{= it.fields.name }}</a></li>",
            evalText = doT.template(tpl),
            content = "";
        $.each(data, function (i, item) {
            content += evalText(item)
        });
        $("#product_ul").html(content);
        init_product_click();
    });
}

function init_product_click() {
    $(".product").each(function () {
        $(this).click(function () {
           var product = $(this).text();
            $("#show_product").text(product);
            $("#show_product").attr('p_id', $(this).attr('p_id'));
        });
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

function init_graph() {
    var aspect_sentiment = echarts.init($("#aspect_sentiment").get(0)),
        hierarchy_top = echarts.init($("#hierarchy_top").get(0)),
        hierarchy_low = echarts.init($("#hierarchy_low").get(0)),
        hierarchy_dict = JSON.parse(localStorage.getItem("hierarchy")),
        all_aspect_senti = JSON.parse(localStorage.getItem("aspect_sentiment"));
    var keys = Object.keys(hierarchy_dict);
    var sdic = Object.keys(hierarchy_dict).sort(function (a,b) {return hierarchy_dict[b]['count'] - hierarchy_dict[a]['count']})
    var hierarchy_key = sdic.slice(0, 8);
    var hierarchy_value = [],
        indicator = [];
    for (var i in hierarchy_key)
    {
        hierarchy_value.push(hierarchy_dict[hierarchy_key[i]]['sum'] / hierarchy_dict[hierarchy_key[i]]['count'])
        indicator.push({text:hierarchy_key[i], max:2, min:-2})
    }

    var option_hierarchy = {
            title : {
                text: '手机属性'
            },
            tooltip : {
                trigger: 'axis'
            },
            polar : [
               {
                   indicator : indicator
                }
            ],
            calculable : true,
            series : [
                {
                    name: '属性情感值',
                    type: 'radar',
                    data : [
                        {
                            value : hierarchy_value,
                            name: '属性情感值'
                        }
                    ]
                }
            ]
        };
    hierarchy_top.setOption(option_hierarchy)
}

function init_confirm_click() {
    $("#confirm").click(function () {
        var brand = $("#show_brand").text(),
            cat = $("#show_cat").text(),
            platform = $("#show_platform").text(),
            product_id = $("#show_product").attr("p_id");
        $.getJSON('../compute/',{'cat':cat, 'platform':platform, 'brand':brand, 'product_id':product_id}, function (data) {
            localStorage.setItem("aspect_sentiment", JSON.stringify(data['result']));
            localStorage.setItem("hierarchy",JSON.stringify(data['hierarchy']));
            init_graph();
        })
    })
}

function init_click() {
    init_cat_click();
    init_platform_click();
    init_brand_click();
    init_confirm_click();
}