var app = app || {};

(function() {
  DealsListView = Backbone.View.extend({
    initialize: function(vd_col) {
      this.vd_col = vd_col;
      console.log(this.vd_col);
      _.bindAll(this, 'addDeals');
      this.vd_col.bind('sync reset', this.addDeals, this);
    },

    render: function() {
      template = _.template($('#dealsListTemplate').html());
      this.$el.html(template);
      console.log(this.vd_col);
      this.addDeals();
      return this;
    },

    addDeals: function() {
      this.$el.find(".deal-list-table").children().remove();
      var self = this;
      _.each(this.vd_col.models, function(deal) {
        console.log("loopin'");
        console.log(deal);
        var view = new app.DealRowView(deal);
        console.log(view);
        self.$el.find(".deal-list-table").append(view.render().el);
      });
    }
  });
})();
