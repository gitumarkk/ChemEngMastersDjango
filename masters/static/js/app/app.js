/*global require*/
'use strict';

require.config({
    // baseUrl: "/",
    waitSeconds: 0,
    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        foundation: {
            deps: ['jquery'],
            exports: 'Foundation'
        },
        'foundation.accordion': {
            deps: ['jquery']
        },
        d3: {
            exports: 'd3'
        },
        handlebars: {
            exports: 'Handlebars'
        },
        "bootstrap-collapse": {
            deps: ['jquery']
        },
        "bootstrap-carousel": {
            deps: ['jquery']
        }
    },

    paths: {
        d3: '../libs/d3/d3',
        jquery: '../libs/jquery/dist/jquery',
        underscore: '../libs/underscore/underscore',
        backbone: '../libs/backbone/backbone',
        foundation: '../libs/foundation/js/foundation.min',
        text: '../libs/requirejs-text/text',
        handlebars: '../libs/handlebars/handlebars.amd',
        "bootstrap-collapse": '../libs/bootstrap/bootstrap/collapse',
        "bootstrap-carousel": '../libs/bootstrap/bootstrap/carousel'
    }
});

require(['jquery', 'foundation'], function($, Foundation) {
    // $('.collapse').collapse()
    $(document).foundation({
        orbit: {
            slide_number: false,
            timer: false,
            bullets: false,
            next_on_click: true
        }
    });
});

require(['jquery', "backbone", "routers/router"], function($, Backbone, AppRouter) {
    // Global Inheritance
    Backbone.View.prototype.close = function() {
        this.remove();
        this.unbind();
        if(this.onClose){
            this.onClose();
        }
    };

    Backbone.View.prototype.getAjax = function(options){
        $.ajax({
            url: options.url,
            type: "GET",
            xhrFields: {
                withCredentials: true
            },
            success: function(response) {
                options.success(response, options);
            },
            error: function(response){
                console.log(response);
            }
        });
    };

    Backbone.View.prototype.postAjax = function(options){
        $.ajax({
            url: options.url,
            data: options.data,
            type: "POST",
            xhrFields: {
                withCredentials: true
            },
            success: function(response) {
                options.success(response, options);
            },
            error: function(response) {
                options.error();
                console.log(response);
            }
        });
    };

    // SserializeObject for forms

    $.fn.serializeObject = function(){
        var o = {};
        var a = this.serializeArray();

        $.each(a, function(){
            if (o[this.name] !== undefined) {
                if(!o[this.name].push){
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || "");
            } else {
                o[this.name] = this.value || "";
            }
        });
        return o;
    };

    $(document).ready(function() {
        Backbone.history.start();
        var app_router = new AppRouter({silence:true});  // Prevent initial route '' from being invoked
        // alert("ready");
        $("body").find(".loading").remove();
    });
});
