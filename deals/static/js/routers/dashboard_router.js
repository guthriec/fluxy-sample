var app = app || {};

(function() {
  app.DashboardRouter = Backbone.Router.extend({
    routes: {
      "": "index",
      "login": "auth",
      "register": "register",
      "create": "create",
      "view": "view"
    },

    index: function() {
      this.currentView = new app.DashboardIndexView();
      $('#dashboard').html(this.currentView.render().el);
    },

    auth: function() {
      this.currentView = new app.AuthView();
      $('#dashboard').html(this.currentView.render().el);
    },

    register: function() {
      this.currentView = new app.RegView();
      $('#dashboard').html(this.currentView.render().el);
    },

    create: function() {
      this.currentView = new app.DealCreateView();
      // This should be done in DealCreateView, but the whole vendor thing is broken anyway
      this.currentView.setVendor(app.currentVendor);
      $('#dashboard').html(this.currentView.render().el);
    },

    view: function() {
      var deals_col = new app.VendorDealCollection();
      deals_col.set_vendor(app.currentVendor);
      this.currentView = new app.DealsListView(deals_col);
      $('#dashboard').html(this.currentView.render().el);
      deals_col.fetch();
    }
  });
})();
