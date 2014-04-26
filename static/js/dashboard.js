// Start the dashboard Marionette/Backbone app
DashboardApp = new Backbone.Marionette.Application();

// Add the events initializer first
DashboardApp.addInitializer(function(options) {
  DashboardApp.events = _.extend({}, Backbone.Events);
});

// Register the main dashboard region
DashboardApp.addRegions({
  dashboardRegion: '#dashboard-container',
  leftNavbarRegion: '#left-navbar-container',
  modalRegion: '#modal-container'
}),

DashboardApp.addInitializer(function(options) {
  var modalControllerView = new DashboardApp.ModalControllerView();
  DashboardApp.modalRegion.show(modalControllerView);
});



DashboardApp.addInitializer(function(options) {
  var leftNavView = new DashboardApp.LeftNavView();
  DashboardApp.leftNavbarRegion.show(leftNavView);
});

/*
 * @author: Chris, Ayush
 * @desc: a Marionette layout that warps the main content of the dashboard.
 *        Expects to be initalized with a complete set of collections for
 *        every dashboard view. Handles navigation within the dashboard.
 */
DashboardApp.MainContent = Backbone.Marionette.Layout.extend({
  template: "#main-content-template",

  regions: {
    dashboard: '#dashboard'
  },

  initialize: function(options) {
    DashboardApp.events.on('showCreateView', this.showCreate, this);
    DashboardApp.events.on('showReviveView', this.showRevive, this);
    DashboardApp.events.on('showReviewView', this.showReview, this);
    DashboardApp.events.on('showActiveView', this.showActive, this);

    this.deals = options.deals;
    this.scheduledDeals = this.deals.scheduledCollection();
    this.expiredDeals = this.deals.expiredCollection();
    this.activeDeals = this.deals.activeCollection();
    this.activeDealsCollectionView = new DashboardApp.DealsCollectionView({
      collection: this.activeDeals
    });
    this.scheduledDealsCollectionView = new DashboardApp.DealsCollectionView({
      collection: this.scheduledDeals
    });
    this.expiredDealsCollectionView = new DashboardApp.DealsCollectionView({
      collection: this.expiredDeals
    });
    this.dealCreateForm = new DashboardApp.DealCreateFormView();
  },


  showCreate: function() {
    this.dashboard.show(this.dealCreateForm);
  },

  showRevive: function() {
    this.dashboard.show(this.expiredDealsCollectionView);
  },

  showReview: function() {
    this.dashboard.show(this.scheduledDealsCollectionView);
  },

  showActive: function() {
    this.dashboard.show(this.activeDealsCollectionView);
  },

  onShow: function() {
    this.dashboard.show(this.dealCreateForm);
  },
});

// Load the initializer
DashboardApp.addInitializer(function(options) {
  var opts = {};
  opts.deals = new DashboardApp.DealsCollection([], { 'vendorId': vendorId, 'listenForCreate': true });
  opts.deals.fetch({ reset: true });

  var mainContent = new DashboardApp.MainContent(opts);
  DashboardApp.dashboardRegion.show(mainContent);
});

$(document).ready(function() {
  DashboardApp.start();
});
