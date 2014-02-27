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
    $('#dashboard').html(this.currentView.render().el);
  },

  view: function() {
    this.currentView = new DealListView();
    $('#dashboard').html(this.currentView.render().el);
  }
});
