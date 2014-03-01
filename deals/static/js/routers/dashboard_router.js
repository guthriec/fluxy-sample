DashboardRouter = Backbone.Router.extend({
  routes: {
    "": "index",
    "create": "create",
    "view": "view"
  },

  index: function() {
    this.currentView = new DashboardIndexView();
    $('#dashboard').html(this.currentView.render().el);
  },

  create: function() {
    this.currentView = new DealCreateView();
    this.currentView.setVendor(1);
    $('#dashboard').html(this.currentView.render().el);
  },

  view: function() {
    var deals_col = new VendorDealCollection();
    deals_col.set_vendor(1);
    this.currentView = new DealsListView(deals_col);
    $('#dashboard').html(this.currentView.render().el);
    deals_col.fetch();
  }
});
