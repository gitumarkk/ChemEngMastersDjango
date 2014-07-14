define([
"backbone",
"handlebars",
"d3",
"utils/d3_graphs",
"text!tpl/graph-view.html"],
function(Backbone, Handlebars, d3, d3_graphs, graphTPL){
    'use strict';

    var GraphView = Backbone.View.extend({
        template: graphTPL,
        events: {},

        initialize: function(options){
            var self = this;
            self.data = options.data;
            self.section = options.section;
            self.compiled_template = this.compileTemplate();
            self.render();
        },

        render: function() {
            var self = this;
            self.renderTemplate();
            self.plotGraphs();
            return self;
        },
        renderTemplate: function(){
            var self = this;
            var data = {
                bioxidation : true ? self.section === "bioxidation" : false,
                chemical : true ? self.section === "chemical" : false,
                section: self.section
            };
            self.$el.html(this.compiled_template(data));
            return self;
        },
        plotGraphs: function(){
            var self = this;
            self.ferricGraphs();
            self.metalIonGraphs("Cu", "copper");
            self.metalIonGraphs("Sn", "tin");
            self.metalIonGraphs("Zn", "zinc");
            if (self.section === "chemical") {
                self.metalGraphs("Cu", "copper");
                self.metalGraphs("Sn", "tin");
                self.metalGraphs("Zn", "zinc");
            }
            return self;
        },
        ferricGraphs: function(){
            var self = this;
            var ferrous_obj = d3_graphs();
            ferrous_obj.graph_container("#"+self.section+"-ferrous-out");
            ferrous_obj.add_ferrous_data(self.data);

            var ferric_obj = d3_graphs();
            ferric_obj.graph_container("#"+self.section+"-ferric-out");
            ferric_obj.add_ferric_data(self.data);

            // var ferrous_obj_in = d3_graphs();
            // ferrous_obj_in.graph_container("#"+self.section+"-ferrous-in");
            // ferrous_obj_in.add_ferrous_data_in(self.data);

            // var ferric_obj_in = d3_graphs();
            // ferric_obj_in.graph_container("#"+self.section+"-ferric-in");
            // ferric_obj_in.add_ferric_data_in(self.data);

            return self;
        },
        metalGraphs: function(symbol, name){
            var self = this;
            var obj = d3_graphs();
            obj.graph_container("#"+self.section+"-"+name);
            obj.append_metal(self.data, symbol, name);
            return self;
        },
        metalIonGraphs: function(symbol, name){
            var self = this;
            var obj = d3_graphs();
            obj.graph_container("#"+self.section+"-"+name+"-ion");
            obj.append_metal_ion(self.data, symbol, name);
            return self;
        },
        compileTemplate: function() {
            var self = this;
            var tpl;
            tpl = Handlebars.default.compile(self.template);
            return tpl;
        }
    });

    return GraphView;
});
