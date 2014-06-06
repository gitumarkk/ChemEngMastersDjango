define([
"backbone",
"handlebars",
"text!tpl/summary-view.html",],
function(Backbone, Handlebars, summaryTPL){
    var SummaryView = Backbone.View.extend({
        el: "#summary-container",
        template: summaryTPL,

        initialize: function(options){
            var self = this;

            self.data = options.data;
            self.compiled_template = this.compileTemplate();
            self.render();
        },
        render: function(){
            var self = this;
            self.$el.html(this.compiled_template(self.data));
            return self;
        },
        compileTemplate: function() {
            var self = this;
            var tpl;
            tpl = Handlebars.default.compile(self.template);
            return tpl;
        },
    });
    return SummaryView;
});
