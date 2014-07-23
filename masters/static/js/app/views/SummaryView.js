define([
"backbone",
"handlebars",
"d3",
"utils/d3_graphs",
"text!tpl/summary-view.html"],
function(Backbone, Handlebars, d3, d3_graphs, summaryTPL){
    var SummaryView = Backbone.View.extend({
        el: "#summary-container",
        template: summaryTPL,
        events: "",

        initialize: function(options){
            var self = this;

            self.data = options.data;
            self.compiled_template = this.compileTemplate();
            self.render();
        },
        render: function(){
            var self = this;
            self.$el.html(this.compiled_template(self.data));
            self.summaryGraphs();
            return self;
        },
        summaryGraphs: function(){
            var self = this;
            var obj = d3_graphs();
            obj.graph_container("#rate-ratio");
            obj.add_rate_ratio(self.data.data);
            return self;
        },
        compileTemplate: function() {
            var self = this;
            var tpl;
            tpl = Handlebars.default.compile(self.template);
            return tpl;
        }
    });
    return SummaryView;
});
