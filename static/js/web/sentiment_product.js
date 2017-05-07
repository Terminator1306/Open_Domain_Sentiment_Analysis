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
    $.getJSON("../get_product", {'cat': cat, 'platform': platform, 'brand': brand}, function (data) {
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
            $("#show_product").text(product.slice(0,28));
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
            if (cat && platform) {
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
            if (cat && platform) {
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
                barMaxWidth: 30,
                data: hierarchy_value,
                itemStyle: {
                    normal: {
                        color: function (params) {
                            // build a color map as your need.
                            var colorList = [
                                '#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B',
                                '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',
                                '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'
                            ];
                            return colorList[params.dataIndex % 15]
                        }
                    }
                }
            }
        ]
    };
    hierarchy_top.setOption(option);
    hierarchy_top.on('click', function (param) {
        var top_aspect = param.name;
        var aspect_list = [],
            count_list = [],
            value_list = [];
        for (var word in hierarchy_dict[top_aspect]['low']) {
            aspect_list.push(word);
            var each_value = hierarchy_dict[top_aspect]['low'][word];
            count_list.push(each_value.length);
            if (each_value.length > 0) {
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
                data: ['情感值', '评论数']
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
                    barMaxWidth: 30,
                    yAxisIndex: 0,
                    itemStyle: {
                        normal: {
                            color: function () {
                                // build a color map as your need.
                                var colorList = [
                                    '#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B'
                                ];
                                return colorList[Math.floor(Math.random() * 5 + 1)]
                            }
                        }
                    },
                    data: value_list
                },
                {
                    name: '评论数',
                    type: 'bar',
                    barMaxWidth: 30,
                    yAxisIndex: 1,
                    data: count_list,
                    itemStyle: {
                        normal: {
                            color: function () {
                                // build a color map as your need.
                                var colorList = [
                                    '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'
                                ];
                                return colorList[Math.floor(Math.random() * 5 + 1)]
                            }
                        }
                    }
                }
            ]
        };
        hierarchy_low.setOption(low_option);
    });

    var all_aspect = [],
        avg_value = [];
    for (var aspect in all_aspect_senti) {
        all_aspect.push(aspect);
        if (all_aspect_senti[aspect].length > 0) {
            var value = eval(all_aspect_senti[aspect].join('+')) / all_aspect_senti[aspect].length;
            avg_value.push(value.toFixed(2))
        }
    }
    // $("#aspect_sentiment").height(all_aspect.length * 5);
    var all_aspect_option = {
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
        yAxis: [
            {
                type: 'category',
                data: all_aspect
            }
        ],
        xAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '情感值',
                type: 'bar',
                barMaxWidth: 30,
                data: avg_value,
                itemStyle: {
                    normal: {
                        color: function (params) {
                            // build a color map as your need.
                            var colorList = [
                                '#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B',
                                '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',
                                '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'
                            ];
                            return colorList[params.dataIndex % 15]
                        },
                        label: {
                            show: true,
                            position: 'right',
                            formatter: '{b} {c}'
                        }
                    }
                }
            }
        ]
    };
    aspect_sentiment.setOption(all_aspect_option)
}

function init_confirm_click() {
    $("#confirm").click(function () {
        var brand = $("#show_brand").text(),
            cat = $("#show_cat").text(),
            platform = $("#show_platform").text(),
            product_id = $("#show_product").attr("p_id");
        $.getJSON('../compute/', {
            'cat': cat,
            'platform': platform,
            'brand': brand,
            'product_id': product_id
        }, function (data) {
            localStorage.setItem("aspect_sentiment", JSON.stringify(data['result']));
            localStorage.setItem("hierarchy", JSON.stringify(data['hierarchy']));
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