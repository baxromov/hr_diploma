// Rainfall and Evaporation
$(function() {
    "use strict";
    var app = {};
    var option = {};
    var rainFall = getChart("echart-rainfall");
    option = {
        legend: {
            data:['Keldi','Kechikdi','Kelmadi'],
            bottom: '0',
        },
        grid: {
            left: '5%',
            right:'0%',
            top: '2%',
            bottom:'15%',
        },
        tooltip : {
            trigger: 'axis'
        },
        calculable : true,

        xAxis : {
            type : 'category',
            data : ['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sept','Oct','Nov','Dec'],
            axisLine:{
                lineStyle:{
                    color: '#f8f9fa',
                }
            },
            axisLabel: {
                color: '#4D5052',
            }
        },
        yAxis : {
            type : 'value',
            splitLine: {
                lineStyle:{
                    color: '#f8f9fa',
                }
            },
            axisLine:{
                lineStyle:{
                    color: '#f8f9fa',
                }
            },
            axisLabel: {
                color: '#4D5052',
            }
        },
        series : [
            {
                name:'Keldi',
                type:'bar',
                color: '#45e5c3',
                data:[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
                markPoint : {
                    data : [
                        {type : 'max', name: 'Max'},
                        {type : 'min', name: 'Min'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: 'Average'}
                    ]
                }
            },
            {
                name:'Kechikdi',
                type:'bar',
                color: '#288cff',
                data:[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
                markPoint : {
                    data : [
                        {name : 'Highest', value : 182.2, xAxis: 7, yAxis: 183},
                        {name : 'Minimum', value : 2.3, xAxis: 11, yAxis: 3}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name : 'Average'}
                    ]
                }
            },
            {
                name:'Kelmadi',
                type:'bar',
                color: '#ff758e',
                data:[3.5, 9.5, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
                markPoint : {
                    data : [
                        {name : 'Highest', value : 100, xAxis: 7, yAxis: 100},
                        {name : 'Minimum', value : 5, xAxis: 11, yAxis: 3}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name : 'Average'}
                    ]
                }
            }
        ]
    };
    if (option && typeof option === "object") {
        rainFall.setOption(option, true);
    }
    $(window).on('resize', function(){
        rainFall.resize();
    });
});

// Doughnut Chart
$(function() {
    "use strict";
    var doughnutChart = getChart("echart-doughnut");
    var app = {};
    var option = {};

    option = {
        grid: {
            left: '5%',
            right:'0%',
            top: '2%',
            bottom:'5%',
        },
        
        legend: {
            orient: 'vertical',
            x: 'left',
            data:['Ishga kechikdi 15','Ishga kelmadi 10','Ishga keldi 75']
        },
        series: [
            {
                name:'Access source',
                type:'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:[
                    {value:15, name:'Ishga kechikdi 15', itemStyle: {color: '#ffc323',}},
                    {value:10, name:'Ishga kelmadi 10', itemStyle: {color: '#ff758e',}},
                    {value:75, name:'Ishga keldi 75', itemStyle: {color: '#49c5b6',}},
                ]
            }
        ]
    };
    if (option && typeof option === "object") {
        doughnutChart.setOption(option, true);
    }
    $(window).on('resize', function(){
        doughnutChart.resize();
    });
});


function getChart(id){
    var dom = document.getElementById(id);
    return echarts.init(dom);
}