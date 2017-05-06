/**
 * Created by 87459 on 2017/5/5.
 */
function load_bar(val, aspect) {
    var bar = echarts.init($("#result").get(0));
    var option = {
        title: {
            text: '各属性情感值'
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                data: aspect
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
                data: val,
                itemStyle: {
                    normal: {
                        color: function (params) {
                            // build a color map as your need.
                            var colorList = [
                                '#C1232B', '#B5C334', '#FCCE10', '#E87C25', '#27727B',
                                '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',
                                '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'
                            ];
                            return colorList[Math.floor(Math.random()*15+1)]
                        }
                    }
                }
            }
        ]
    };
    bar.setOption(option);
}

function init_confirm() {
    $("#confirm").click(function () {
        var data = {};
        data.comment = $("#comment").val();
        $("#confirm").text("计算中");
        $("#confirm").attr("disabled", true);
        $.getJSON("../compute/comment/", data, function (data) {
            load_bar(data.value, data.aspect);
            $("#confirm").text("确定");
            $("#confirm").attr("disabled", false);
        });
    });
}

function init_cat() {
    $(".cat").each(function () {
        $(this).click(function () {
            $("#show_cat").text($(this).text())
        })
    });
}

function init() {
    init_cat();
    init_confirm();
}
