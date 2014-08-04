define([
"backbone",
"handlebars",
"d3",
"text!tpl/rates.html",
"text!tpl/rates_table.html",
"text!tpl/rates_constant.html"
], function(Backbone, Handlebars, d3, TPL, ratesTable, ratesConstant){
    var RatesView = Backbone.View.extend({
        template: TPL,
        el: "#rates_layout",
        events: {

        },
        initialize: function(options){
            var self = this;
            self.src = options.src;
            self.section = options.section;
            self.compiled_template = self.compileTemplate(self.template);
            self.table_template = self.compileTemplate(ratesTable);
            self.constants_template = self.compileTemplate(ratesConstant);

            _.bindAll(self,
                      "manageData");

            self.metals_symbols = ["Cu", "Zn", "Sn"];
            return self;
        },
        render: function(){
            var self = this;

             _options = {
                url: self.src,
                success: self.manageData,
                error: undefined
            };
            self.getAjax(_options);
            return self;
        },
        manageData: function(response, options){
            var self = this;

            self.$el.html(this.compiled_template(response));
            // self.renderTables(response.data);
            self.addData(response);
            return self;
        },
        addData: function(data){
            var self = this;
            var item, metal_data, metal_i, table_html, rates_constant;

            for (item in self.metals_symbols ) {
                metal_symbol = self.metals_symbols[item];
                metal_data = data[self.metals_symbols[item]].data;
                rates_constant = data[self.metals_symbols[item]].rates_constant;
                console.log(rates_constant);
                for (metal_i in metal_data) {
                    table_html = self.table_template({"result": metal_data[metal_i]});
                    self.$el.find("#"+metal_symbol+"-data").append(table_html);
                }
                self.$el.find("#"+metal_symbol+"-data").append(self.constants_template({"result": rates_constant}));
            }
            return self;
        },
        renderTables: function(data, options){
            var self = this;
            var cu_table = self.$el.find("#Cu-table");
            cu_table.html();
            return self;
        },
        renderGraphs: function(data, options){
            var self = this;
            return self;
        },

        // toFixed: function (number, digits) {
        //     return number.toFixed(digits);
        //   },
        compileTemplate: function(_tpl) {
            var self = this;
            tpl = Handlebars.default.compile(_tpl);

            Handlebars.default.registerHelper('truncate_int', function(value, digits) {
              return value.toFixed(digits);
            });

            Handlebars.default.registerHelper('parse_k', function(value, position, digits) {
              return value[position].toFixed(digits);
            });

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
    return RatesView;
});
