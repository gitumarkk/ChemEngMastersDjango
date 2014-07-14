/*
* The Layout is use dto manage the views in a single url route
* It gets the route action, gets the data and renders the different
* graph views depending on the data returned
* At the moment it is used in the reactor system and not individual graphs
*/
define([
"backbone",
"handlebars",
"d3",
"views/SystemView",
"views/SummaryView",
"text!tpl/layout.html"
],
function(Backbone, Handlebars, d3, SystemView, SummaryView, layoutTPL){
    var LayoutView = Backbone.View.extend({
        menuTemplate: layoutTPL,
        el: "#layout",
        // tagName: "div",
        // id: "layout",
        events: {
            "submit #reactor_conditions": "validateForm",
            "change #reactor_conditions": "updateExportData",
            "keyup #reactor_conditions": "updateExportData",
            "click #reactor_conditions [type='checkbox']": "toggleMetalInput",

        },  // Add menu here
        initialize: function(options){
            var self = this;

            // If anything is in DOM completely close it
            // self.close();

            self.current_views = [];
            _.bindAll(self, "assignViews");
            self.type = options.type;
            self.system = options.system;
            self.src = options.src;
            self.menu_tpl = this.compileTemplate(this.menuTemplate);
            self.render();
            // self.fetchDataWithD3();
        },

        render: function(){
            var self = this;
            self.$el.html(self.menu_tpl({system : self.system}));
            return self;
        },

        validateForm: function(ev){
            var self = this;
            var params, reactorConditions;

            ev.preventDefault();
            ev.stopPropagation();

            reactorConditions = $(ev.currentTarget).serializeObject();
            params =  $.param(reactorConditions);

            // Update the export data urls
            //


            this.fetchDataWithD3(self.src+"?"+params);
        },

        fetchDataWithD3: function(url){
            var self = this;
            self.emptyCurrentViews();
            d3.json(url, function(error, data){
                console.log("success fetching data");
                console.log(error);
                self.assignViews(data);
            });
        },

        updateExportData: function(ev){
            var self = this;
            reactorConditions = $(ev.currentTarget).serializeObject();
            params =  $.param(reactorConditions);
            self.$el.find("#export_data").prop("href", "/export_data/" + self.system + "/?" + params);
        },

        toggleMetalInput: function(ev){
            var self = this;
            var $checkbox = $(ev.currentTarget);

            var metal_name = $checkbox.attr("class");
            $metal_input = self.$el.find("#reactor_conditions #"+ metal_name);
            if ($metal_input.attr('disabled')) {
                $metal_input.removeAttr('disabled');
            } else {
                $metal_input.attr('disabled', 'disabled');
                $metal_input.val(0.0);
            }
            return self;
        },

        /*
        This view generates the required views based on the data coming form the back end
        */
        assignViews: function(data){
            var self = this;

            var summary = new SummaryView({data: data.summary});
            var bioxidation = new SystemView({data: data.bioxidation,
                                            section: "bioxidation",
                                            el: "#bioxidation-container"});

            var chemical = new SystemView({data: data.chemical,
                                         section: "chemical",
                                         el: "#chemical-container"});
            self.current_views.push(summary, bioxidation, chemical);
            // $(window).trigger('resize');
            // $('.carousel').carousel();
        },
        compileTemplate: function(_tpl) {
            var self = this;
            var tpl;
            tpl = Handlebars.default.compile(_tpl);
            return tpl;
        },
        closeCurrentViews: function(){
            /* Close all current vies and empty the array */
            var self = this;
            while(self.current_views.length > 0){
                var _v = self.current_views.pop();
                _v.close();
            }
        },

        emptyCurrentViews: function(){
            /* Close all current vies and empty the array */
            var self = this;
            while(self.current_views.length > 0){
                var _v = self.current_views.pop();
                _v.$el.empty();
            }
        },
    });
    return LayoutView;
});
