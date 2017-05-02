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

function init_graph() {
    var aspect_sentiment = echarts.init($("#aspect_sentiment").get(0)),
        hierarchy_top = echarts.init($("#hierarchy_top").get(0)),
        hierarchy_low = echarts.init($("#hierarchy_low").get(0)),
        hierarchy_dict = JSON.parse(localStorage.getItem("hierarchy")),
        all_aspect_senti = JSON.parse(localStorage.getItem("aspect_sentiment"));
    var sdic = Object.keys(hierarchy_dict).sort(function (a, b) {
        return hierarchy_dict[b]['count'] - hierarchy_dict[a]['count']
    });
    var hierarchy_key = sdic.slice(0, 15);
    var hierarchy_value = [],
        indicator = [];
    for (var i in hierarchy_key) {
        var value = hierarchy_dict[hierarchy_key[i]]['sum'] / hierarchy_dict[hierarchy_key[i]]['count'];
        hierarchy_value.push(value.toFixed(2));
        indicator.push({text: hierarchy_key[i], max: 2, min: -2})
    }

    var option_hierarchy = {
        title: {
            text: '手机属性'
        },
        tooltip: {
            trigger: 'axis',
            show: true,
            formatter: '{a}:{b}'
        },
        polar: [
            {
                indicator: indicator
            }
        ],
        calculable: true,
        series: [
            {
                clickable: true,
                name: '属性情感值',
                itemStyle: {
                    normal: {
                        label: {
                            show: true,
                            textStyle: {
                                color: '#800080'
                            }
                        },
                        normal: {
                            color: 'blue'
                        }
                    }
                },
                type: 'radar',
                data: [
                    {
                        value: hierarchy_value,
                        name: '属性情感值'
                    }
                ]
            }
        ]
    };

    var option = {
        title: {
            text: '高层属性情感值',
            subtext: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['情感值']
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                data: hierarchy_key
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '情感值',
                type: 'bar',
                data: hierarchy_value
            }
        ]
    };
    hierarchy_top.setOption(option);
    hierarchy_top.on('click', function (param) {
        var top_aspect = param.name;
        var aspect_list = [],
            count_list = [],
            value_list = [];
        for (var word in hierarchy_dict[top_aspect]['low'])
        {
            aspect_list.push(word);
            var each_value = hierarchy_dict[top_aspect]['low'][word];
            count_list.push(each_value.length);
            if(each_value.length > 0)
            {
                var v = eval(each_value.join('+')) / each_value.length;
                value_list.push(v.toFixed(2));
            }
            else
                value_list.push(0);
        }
        var low_option = {
                title: {
                    text: '低层属性情感值',
                    subtext: top_aspect
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['情感值','评论数']
                },
                calculable: true,
                xAxis: [
                    {
                        type: 'category',
                        data: aspect_list
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: '情感值'
                    },
                    {
                        type: 'value',
                        name: '评论数'
                    }
                ],
                series: [
                    {
                        name: '情感值',
                        type: 'bar',
                        yAxisIndex:0,
                        data: value_list
                    },
                    {
                        name:'评论数',
                        type: 'bar',
                        yAxisIndex:1,
                        data: count_list
                    }
                ]
            };
        hierarchy_low.setOption(low_option);
    });

    var all_aspect = [],
        avg_value = [];
    for (var aspect in all_aspect_senti ){
        all_aspect.push(aspect);
        if(all_aspect_senti[aspect].length > 0)
        {
            var value = eval(all_aspect_senti[aspect]).join('+') / all_aspect_senti[aspect].length;
            avg_value.push(value.toFixed(2))
        }
    }
    var all_aspect_option={
        title: {
            text: '所有属性情感值',
            subtext: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['情感值']
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                data: all_aspect
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '情感值',
                type: 'bar',
                data: avg_value
            }
        ]
    };
    aspect_sentiment.setOption(all_aspect_option)
}

function init_confirm_click() {
    $("#confirm").click(function () {
        var brand = $("#show_brand").text(),
            cat = $("#show_cat").text(),
            platform = $("#show_platform").text();
        $.getJSON('../compute/',{'cat':cat, 'platform':platform, 'brand':brand}, function (data) {
            localStorage.setItem("aspect_sentiment", data['result']);
            localStorage.setItem("hierarchy",data['hierarchy']);
            init_graph()
        })
    })
}

function init_click() {
    init_brand_click();
    init_cat_click();
    init_platform_click();
    init_confirm_click();
}