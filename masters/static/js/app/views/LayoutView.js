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
"views/GraphViewUpdate",
"views/SummaryView",
"text!tpl/layout.html"
],
function(Backbone, Handlebars, d3, GraphView, SummaryView, layoutTPL){
    var LayoutView = Backbone.View.extend({
        menuTemplate: layoutTPL,
        el: "#layout",
        events: {
            "submit #reactor_conditions": "validateForm",
        },  // Add menu here
        initialize: function(options){
            var self = this;

            // If anything is in DOM completely close it
            self.close();

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
            self.$el.html(self.menu_tpl);
            return self;
        },

        validateForm: function(ev){
            var self = this;
            var params, reactorConditions;

            ev.preventDefault();
            ev.stopPropagation();

            reactorConditions = $(ev.currentTarget).serializeObject();
            params =  $.param(reactorConditions);

            this.fetchDataWithD3(self.src+"?"+params);
        },

        fetchDataWithD3: function(url){
            var self = this;
            self.closeCurrentViews();
            d3.json(url, function(error, data){
                self.assignViews(data);
            });
        },

        /*
        This view generates the required views based on the data coming form the back end
        */
        assignViews: function(data){
            var self = this;

            var summary = new SummaryView({data: data.summary});
            var bioxidation = new GraphView({data: data.bioxidation,
                                            section: "bioxidation",
                                            el: "#bioxidation-container"});

            var chemical = new GraphView({data: data.chemical,
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
            console.log("closing all current views");
            console.log(self.current_views.length);
            while(self.current_views.length > 0){
                var _v = self.current_views.pop();
                _v.close();
            }
            console.log(self.current_views.length);
            // for (var _v in self.current_views){
            //     _v.close();
            // }
        }
    });
    return LayoutView;
});
