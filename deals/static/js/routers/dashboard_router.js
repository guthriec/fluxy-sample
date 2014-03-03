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
    
      // Right now vendor is always '1'. The app should have some
      // option to change the current vendor.
      this.currentView.setVendor(1);
      $('#dashboard').html(this.currentView.render().el);
    },

    view: function() {
      var deals_col = new app.VendorDealCollection();
      
      // See note above about determining the right vendor to set.
      deals_col.set_vendor(1);
      this.currentView = new app.DealsListView(deals_col);
      $('#dashboard').html(this.currentView.render().el);
      deals_col.fetch();
    }
  });
})();
