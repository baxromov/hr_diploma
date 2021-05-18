$(function() {
    "use strict";
    skinChanger();
    CustomScrollbar();
    initSparkline();
    initCounters();
    CustomPageJS();
});
// Sparkline
function initSparkline() {
    $(".sparkline").each(function() {
        var $this = $(this);
        $this.sparkline('html', $this.data());
    });
}

// Counters JS 
function initCounters() {
    $('.count-to').countTo();
}

//Skin changer
function skinChanger() {
    $('.right-sidebar .choose-skin li').on('click', function() {
        var $body = $('body');
        var $this = $(this);

        var existTheme = $('.right-sidebar .choose-skin li.active').data('theme');
        $('.right-sidebar .choose-skin li').removeClass('active');
        $body.removeClass('theme-' + existTheme);
        $this.addClass('active');
        $body.addClass('theme-' + $this.data('theme'));
    });
}

// All Custom Scrollbar JS
function CustomScrollbar() {
    // $('.sidebar .menu .list').slimscroll({
    //     height: 'calc(100vh - 20px)',
    //     color: 'rgba(0,0,0,0.1)',
    //     position: 'left',
    //     size: '2px',
    //     alwaysVisible: false,
    //     borderRadius: '3px',
    //     railBorderRadius: '0'
    // });

    $('.right_menu .slim_scroll').slimscroll({
        height: 'calc(100vh - 30px)',
        color: 'rgba(0,0,0,0.1)',
        position: 'right',
        size: '2px',
        alwaysVisible: false,
        borderRadius: '3px',
        railBorderRadius: '0'
    });

    $('.cwidget-scroll').slimscroll({
        height: '306px',
        color: 'rgba(0,0,0,0.4)',
        size: '2px',
        alwaysVisible: false,
        borderRadius: '3px',
        railBorderRadius: '2px'
    });
    
    $('.right-sidebar .slim_scroll').slimscroll({
        height: 'calc(100vh - 100px)',
        color: 'rgba(0,0,0,0.4)',
        size: '2px',
        alwaysVisible: false,
        borderRadius: '3px',
        railBorderRadius: '0'
    });
   
}

function CustomPageJS() {
    $(".boxs-close").on('click', function(){
        var element = $(this);
        var cards = element.parents('.card');
        cards.addClass('closed').fadeOut();
    });

    // Theme Light and Dark  ============
    $('.theme-light-dark .t-dark').on('click', function() {
        $('body').toggleClass('menu_dark');
    });
    $(".menu-sm").on('click',function() {
        $("body").toggleClass("menu_sm");
    });

    // Right bar open close  ============
    $(".minileftbar .notifications").on('click',function() {
        $(".right_menu .notif-menu").toggleClass("open stretchRight").siblings().removeClass('open stretchRight');
        if ($(".right_menu .notif-menu").hasClass('open')) {
            $('.overlay').fadeIn();
        } else {
            $('.overlay').fadeOut();
        }
    });

    $(".minileftbar .task").on('click',function() {
        $(".right_menu .task-menu").toggleClass("open stretchRight").siblings().removeClass('open stretchRight');
        if ($(".right_menu .task-menu").hasClass('open')) {
            $('.overlay').fadeIn();
        } else {
            $('.overlay').fadeOut();
        }
    });

    $(".minileftbar .menuapp-btn").on('click',function() {
        $(".right_menu .menu-app").toggleClass("open stretchRight").siblings().removeClass('open stretchRight');
        if ($(".right_menu .menu-app").hasClass('open')) {
            $('.overlay').fadeIn();
        } else {
            $('.overlay').fadeOut();
        }
    });

    $(".minileftbar .js-right-sidebar").on('click',function() {
        $(".right_menu #rightsidebar").toggleClass("open stretchRight").siblings().removeClass('open stretchRight');
        if ($(".right_menu #rightsidebar").hasClass('open')) {
            $('.overlay').fadeIn();
        } else {
            $('.overlay').fadeOut();
        }
    });
    
    $('.minileftbar .bars').on('click',function() {
        $('.right_menu .sidebar').toggleClass("open stretchRight").siblings().removeClass('open stretchRight');
        if ($('.right_menu .sidebar').hasClass('open stretchRight')) {
            $('.overlay').fadeIn();
        } else {
            $('.overlay').fadeOut();
        }
    });

    $('.overlay').on('click',function() {
        $('.open.stretchRight').removeClass('open stretchRight');
        $(this).fadeOut();
    });

    // Search with sortcut menu ===    
    $(".btn_overlay").on('click',function(){
        $(".overlay_menu").fadeToggle(200);
        $(this).toggleClass('btn-open').toggleClass('btn-close');
    });
    
    $('.overlay_menu .btn').on('click', function(){
        $(".overlay_menu").fadeToggle(200);   
        $(".overlay_menu button.btn").toggleClass('btn-open').toggleClass('btn-close');
        open = false;
    });
    
    //=========
    $('.form-control').on("focus", function() {
        $(this).parent('.input-group').addClass("input-group-focus");
    }).on("blur", function() {
        $(this).parent(".input-group").removeClass("input-group-focus");
    });
}


// Wraptheme Website live chat widget js please remove on your project
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/5c6d4867f324050cfe342c69/default';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();