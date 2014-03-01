var app = app || {};

(function() {
  app.DashboardRouter = Backbone.Router.extend({
    routes: {
      "": "index",
      "create": "create",
      "view": "view"
    },

    index: function() {
      this.currentView = new app.DashboardIndexView();
      $('#dashboard').html(this.currentView.render().el);
    },

    create: function() {
      this.currentView = new app.DealCreateView();
      this.currentView.setVendor(1);
      $('#dashboard').html(this.currentView.render().el);
    },

    view: function() {
      var deals_col = new app.VendorDealCollection();
      deals_col.set_vendor(1);
      this.currentView = new app.DealsListView(deals_col);
      $('#dashboard').html(this.currentView.render().el);
      deals_col.fetch();
    }
  });
})();
