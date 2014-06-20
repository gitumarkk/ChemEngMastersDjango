define(["d3"], function(d3){
    var d3_graphs = function(){
        return {
            graph_container: function(el){
                var self = this;

                self.graph_container = d3.select(el);

                self.parent_width = parseInt(self.graph_container.style('width'), 10);
                self.margin = {top: 20, right: 20, bottom: 50, left: 100};
                self.width = self.parent_width - self.margin.left - self.margin.right;
                self.height = 500 - self.margin.top - self.margin.bottom;

                self.x = d3.scale.linear().range([0, self.width]);
                self.y = d3.scale.linear().range([self.height, 0]);

                self.xAxis = d3.svg.axis()
                    .scale(self.x)
                    .ticks(10)
                    .orient("bottom");

                self.yAxis = d3.svg.axis()
                    .scale(self.y)
                    .ticks(5)
                    .orient("left");

                self.svg = self.graph_container.append("svg")
                    .attr("width", self.width + self.margin.left + self.margin.right)
                    .attr("height", self.height + self.margin.top + self.margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + self.margin.left + "," + self.margin.top + ")");

                self.color = d3.scale.category10();

                return self;
            },

            add_ferrous_data_in: function(data){
                var self = this;
                // Magic occures in line 7853 of d3.js
                var ferrous_in = d3.svg.line()
                                    .x(function(d) { return self.x(d.step); })
                                        .y(function(d) { return self.y(d.flow_in.components.ferrous); });

                self.x.domain(d3.extent(data, function(d) { return d.step; }));
                self.y.domain(d3.extent(data, function(d) { return d.flow_in.components.ferrous; }));

                self.svg.append("path")
                            .datum(data)
                                .attr("class", "line")
                                    .style("stroke", "red")
                                        .attr("d", ferrous_in);

                self.svg.append("g")
                    .attr("class", "x axis")
                        .attr("transform", "translate(0," + self.height + ")")
                            .call(self.xAxis)
                                .append("text")
                                    .attr("y", 20)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "start")
                                                .text("Time (Min)");

                self.svg.append("g")
                    .attr("class", "y axis")
                        .call(self.yAxis)
                            .append("text")
                                .attr("transform", "rotate(-90)")
                                    .attr("y", 6)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "end")
                                                .text("[Ferrous Concentration mol/l]");

                return self;
            },

            add_ferrous_data: function(data){
                var self = this;
                // Magic occures in line 7853 of d3.js
                var ferrous_out = d3.svg.line()
                                    .x(function(d) { return self.x(d.step); })
                                        .y(function(d) { return self.y(d.flow_out.components.ferrous); });

                self.x.domain(d3.extent(data, function(d) { return d.step; }));
                self.y.domain(d3.extent(data, function(d) { return d.flow_out.components.ferrous; }));
                // Multi Series Plot

                // var sys_data = self.color.domain().map(function(){

                // });
                // self.y.domain([
                //               d3.min(data, function(c){return d3.min(c.values, function(v){ return v.temperature; });})
                //         ]);

                self.svg.append("path")
                            .datum(data)
                                .attr("class", "line")
                                    .style("stroke", "red")
                                        .attr("d", ferrous_out);

                self.svg.append("g")
                    .attr("class", "x axis")
                        .attr("transform", "translate(0," + self.height + ")")
                            .call(self.xAxis)
                                .append("text")
                                    .attr("y", 20)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "start")
                                                .text("Time (Min)");

                self.svg.append("g")
                    .attr("class", "y axis")
                        .call(self.yAxis)
                            .append("text")
                                .attr("transform", "rotate(-90)")
                                    .attr("y", 6)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "end")
                                                .text("[Ferrous Concentration mol/l]");

                return self;
            },

            add_ferric_data: function (data){
                var self = this;

                var ferric_out = d3.svg.line()
                                    .x(function(d) { return self.x(d.step); })
                                        .y(function(d) { return self.y(d.flow_out.components.ferric); });

                self.x.domain(d3.extent(data, function(d) { return d.step; }));
                self.y.domain(d3.extent(data, function(d) { return d.flow_out.components.ferric; }));

                self.svg.append("path")
                            .datum(data)
                                .attr("class", "line")
                                    .style("stroke", "red")
                                        .attr("d", ferric_out);

                self.svg.append("g")
                    .attr("class", "x axis")
                        .attr("transform", "translate(0," + self.height + ")")
                            .call(self.xAxis)
                                .append("text")
                                    .attr("y", 20)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "start")
                                                .text("Time (Min)");

                self.svg.append("g")
                    .attr("class", "y axis")
                        .call(self.yAxis)
                            .append("text")
                                .attr("transform", "rotate(-90)")
                                    .attr("y", 6)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "end")
                                                .text("[Ferric Concentration mol/m^-3]");

                return self;

            },

            add_ferric_data_in: function (data){
                var self = this;

                var ferric_in = d3.svg.line()
                                    .x(function(d) { return self.x(d.step); })
                                        .y(function(d) { return self.y(d.flow_in.components.ferric); });

                self.x.domain(d3.extent(data, function(d) { return d.step; }));
                self.y.domain(d3.extent(data, function(d) { return d.flow_in.components.ferric; }));

                self.svg.append("path")
                            .datum(data)
                                .attr("class", "line")
                                    .style("stroke", "red")
                                        .attr("d", ferric_in);

                self.svg.append("g")
                    .attr("class", "x axis")
                        .attr("transform", "translate(0," + self.height + ")")
                            .call(self.xAxis)
                                .append("text")
                                    .attr("y", 20)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "start")
                                                .text("Time (Min)");

                self.svg.append("g")
                    .attr("class", "y axis")
                        .call(self.yAxis)
                            .append("text")
                                .attr("transform", "rotate(-90)")
                                    .attr("y", 6)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "end")
                                                .text("[Ferric Concentration mol/m^-3]");

                return self;

            },

            append_copper: function(data){
                var self = this;
                // console.log(data);
                var copper = d3.svg.line()
                                    .x(function(d) { return self.x(d.step); })
                                        .y(function(d) { return self.y(d.ions.Cu); });

                self.x.domain(d3.extent(data, function(d) { return d.step; }));
                self.y.domain(d3.extent(data, function(d) { console.log(d.ions.Cu); return d.ions.Cu; }));

                self.svg.append("path")
                            .datum(data)
                                .attr("class", "line")
                                    .style("stroke", "red")
                                        .attr("d", copper);

                self.svg.append("g")
                    .attr("class", "x axis")
                        .attr("transform", "translate(0," + self.height + ")")
                            .call(self.xAxis)
                                .append("text")
                                    .attr("y", 20)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "start")
                                                .text("Time (Min)");

                self.svg.append("g")
                    .attr("class", "y axis")
                        .call(self.yAxis)
                            .append("text")
                                .attr("transform", "rotate(-90)")
                                    .attr("y", 6)
                                        .attr("dy", ".71em")
                                            .style("text-anchor", "end")
                                                .text("[Copper Concentration mol/m^-3]");

                return self;

            },

            append_cupric: function(data){

            }
        };
    };
    return d3_graphs;
});
