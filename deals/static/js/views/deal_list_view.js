var app = app || {};

/*
 * @author: Chris
 * View for list of deals for a given vendor.
 */
(function(window, document, undefined) {
  app.DealsListView = Backbone.View.extend({
    // Expects a VendorDealsCollection
    initialize: function(vd_col) {
      this.vd_col = vd_col;
      _.bindAll(this, 'addDeals');
      // Re-render the view elements on collection db update
      this.vd_col.bind('sync reset', this.addDeals, this);
    },

    render: function() {
      template = _.template($('#dealsListTemplate').html());
      this.$el.html(template);
      this.addDeals();
      return this;
    },

    addDeals: function() {
      this.$el.find(".deal-list-table").children().remove();
      var self = this;
      _.each(this.vd_col.models, function(deal) {
        var view = new app.DealRowView(deal);
        self.$el.find(".deal-list-table").append(view.render().el);
      });
    }
  });
})(this, this.document);
