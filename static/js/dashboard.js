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

/*
 * @author: Ayush, Chris
 * @desc: Defines the model that represents the deal that is going to be
 * displayed.
 */
DealModel = Backbone.Model.extend({ });

// Utility function for initializing the deals collections
DealCollInit = function(models, options) {
  this.vendorId = options.vendorId || -1;
  DashboardApp.events.on('createDealTrigger', this.create, this);
};

/*
 * @author: Ayush
 * @desc: Defines the collection that represents a grouping of DealModel items.
 * Note: the defined URL is used as a GET request to get a list of deals to be
 * displayed.
 */
DealsCollection = Backbone.Collection.extend({

  model: DealModel,

  initialize: DealCollInit,

  url: function() {
    return '/api/v1/vendor/' + this.vendorId + '/deals/';
  }

});

/*
 * @author: Chris
 * @desc: Like a DealsCollection, but hooks into the /vendor/deals/all endpoint.
 *        This collection also has functions scheduledColl and expiredColl that
 *        return FullDealsCollections filtered into scheduled and expired deals.
 *        These new collections listen to the original collection for changes
 *        and update themselves accordingly.
 */
FullDealsCollection = Backbone.Collection.extend({

  model: DealModel,

  initialize: DealCollInit,

  url: function() {
    return '/api/v1/vendor/' + this.vendorId + '/deals/all/';
  },

  // Filter collection to include only deals that have not started.
  // Potential for client-server synchronization issues.
  scheduled: function() {
    return this.filter(function(deal) {
      return 0 < (new Date(deal.get('time_start') - Date.now()));
    });
  },

  // Returns collection that has only scheduled deals and updates whenever
  // the original FullDealsCollection gets updated.
  scheduledColl: function() {
    var filtered = this.scheduled();
    var scheduledCollection = new FullDealsCollection(filtered, { 'vendorId': this.vendorId });
    var self = this;
    scheduledCollection.listenTo(self, 'add remove reset sync', function() {
      this.reset(self.scheduled(), { 'vendorId' : self.vendorId });
    });
    return scheduledCollection;
  },

  // Filter collection to include only deals that have expired.
  // Pretends we're 1 minute in the future to mitigate synchronization issues.
  expired: function() {
    return this.select(function(deal) {
      return 0 > (new Date(deal.get('time_end')) - Date.now() - 60000);
    });
  },

  // Returns collection that has only expired deals and updates whenever
  // the original FullDealsCollection gets updated.
  expiredColl: function() {
    var filtered = this.expired();
    var expiredCollection = new FullDealsCollection(filtered, { 'vendorId': this.vendorId });
    var self = this;
    expiredCollection.listenTo(self, 'add remove reset sync', function() {
      this.reset(self.expired(), { 'vendorId' : self.vendorId });
    });
    return expiredCollection;
  }
});

/*
 * @author: Ayush
 * @desc: Defines the view that is associated with the DealModel. It represents
 * a DealModel as a <tr> tag.
 */
DealView = Backbone.Marionette.ItemView.extend({
  template: '#deal-template',
  tagName: 'tr',
  className: 'deal'
});

/*
 * @author: Ayush
 * @desc: Defines the view that is associated with DealsCollection. Is
 * responsible for showing all the DealView objects in a <table>.
 */
DealsCollectionView = Backbone.Marionette.CompositeView.extend({
  tagname: 'table',
  id: 'deals-list-view',
  className: 'table table-striped table-bordered',
  template: '#deals-collection-template',
  itemView: DealView,

  collectionEvents: {
    "sync": "render"
  },

  appendHtml: function(collectionView, itemView) {
    collectionView.$('tbody').append(itemView.el);
  }
});

/*
 * @author: Ayush
 * @desc: Responsible for rendering and displaying any necessary modals.
 */
DashboardApp.ModalControllerView = Backbone.Marionette.ItemView.extend({
  template: '#modal-controller-template',

  events: {
    'click #confirm-create-deal-modal #create-btn': 'createDeal',
    'click #confirm-create-deal-modal #cancel-btn': 'cancelCreateDeal'
  },

  initialize: function() {
    DashboardApp.events.on('createDealConfirmTrigger', this.confirmDealCreation, this);
  },

  confirmDealCreation: function(deal) {
    console.log('confirmDealCreation');
    this.newDeal = deal;

    var $modal = this.$el.find('#create-deal-modal');

    $modal.find('#title td:nth-child(2)').html(deal.title);
    $modal.find('#description td:nth-child(2)').html(deal.desc);

    var d = Math.abs((new Date(deal.time_start)) - (new Date(deal.time_end)));
    var hours = parseInt(d / 3600000);
    var minutes = d % 3600000 / 60000;
    $modal.find('#duration td:nth-child(2)').html(hours + 'H ' + minutes + 'M');

    $modal.modal('show');
    console.log('modal has been instructed to show');
  },

  cancelCreateDeal: function() {
    // TODO: send trigger to clear form
    this.$el.find('#create-deal-modal').modal('hide');
  },

  createDeal: function() {
    // TODO: send trigger to clear from
    DashboardApp.events.trigger('createDealTrigger', this.newDeal);
    this.$el.find('#create-deal-modal').modal('hide');
  }

});
DashboardApp.addInitializer(function(options) {
  var modalControllerView = new DashboardApp.ModalControllerView();
  DashboardApp.modalRegion.show(modalControllerView);
});

/*
 * @author: Ayush
 * @desc: Defines the view that is associated with the form that allows vendors
 * to create a new deal. It is responsible for handling all events associated
 * with the form.
 */
DealCreateFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #submit-btn': 'createDeal'
  },
  template: '#deal-create-form-template',

  render: function() {
    this.$el.html(_.template($(this.template).html()));

    // Set up the JQuery UI Spinners

    var currDate = new Date();
    var currDay = currDate.getDate();
    var latestDate = new Date();
    latestDate.setDate(currDay + 7);
    var monthNames = [ "January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November",
                       "December" ]
    var dayNames = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday" ]
    var daySelect = this.$el.find('#start-day');
    daySelect.empty();
    var possibleDay = new Date();
    possibleDay.setHours(0);
    possibleDay.setMinutes(0);
    possibleDay.setSeconds(0);
    possibleDay.setMilliseconds(0);
    for (var i=0; i < 8; i++) {
      possibleDay.setDate(currDay + i);
      daySelect.append('<option value="' + possibleDay.getTime()  + '">' + dayNames[possibleDay.getDay()] + ', ' + monthNames[possibleDay.getMonth()] + ' ' + possibleDay.getDate().toString() + '</option>');
    }

    this.$el.find('input:radio[name="limit"]').change(
      function() {
        if ($(this).is(':checked') && (this).value == 'limited') {
          $('#max-deals-number').prop('disabled', false);
          $('#max-deals-number').attr('placeholder', '1  --  500');
          $('#max-deals-number').attr('maxlength', '3');
        }
        if ($(this).is(':checked') && (this).value == 'unlimited') {
          $('#max-deals-number').prop('disabled', true);
          $('#max-deals-number').attr('placeholder', 'Unlimited');
          $('#max-deals-number').val('');
        }
      }
    );
    return this;
  },

  createDeal: function(e) {
    e.preventDefault();

    var newModel = {};

    var $formInputs = $('#deal-form :input');
    var formValues = {};
    $formInputs.each(function() {
      formValues[this.name] = this.value;
    });
    newModel['title'] = formValues['title'];
    newModel['desc'] = formValues['desc'];
    var timeStart = new Date();
    var startHours = Number(formValues['start-hours']);
    if (formValues['start-am-pm'] == 'pm') {
      startHours += 12;
    } else if (startHours == 12) {
      startHours = 0;
    }
    var startMinutes = Number(formValues['start-minutes']) + 60 * startHours;
    timeStart.setTime(Number(formValues['start-day']) + 60000 * startMinutes);
    newModel['time_start'] = timeStart;
    var minutes = Number(formValues['duration-minutes']) + 60 * Number(formValues['duration-hours']);
    var timeEnd = new Date();
    timeEnd.setTime(timeStart.getTime() + minutes * 60000);
    newModel['time_end'] = timeEnd;
    newModel['max_deals'] = -1;
    var limitRadio = this.$el.find('input:radio[value="limited"]');
    if (limitRadio.is(':checked')) {
      newModel['max_deals'] = Number(formValues['max-deals']);
    }
    newModel['instructions'] = 'Show to waiter';
    console.log(newModel);

    DashboardApp.events.trigger('createDealConfirmTrigger', newModel);
    this.$el.find('#submit-btn').blur();
  }
});

DashboardApp.LeftNavView = Backbone.Marionette.ItemView.extend({
  tagName: 'ul',
  className: 'nav nav-stacked list-group',
  id: 'left-navbar',
  template: '#left-navbar-template',

  events: {
    'click #nav-create': 'showCreate',
    'click #nav-revive': 'showRevive',
    'click #nav-review': 'showReview',
    'click #nav-active': 'showActive'
  },

  showCreate: function(e) {
    e.preventDefault();
    $("#left-navbar").find(".list-group-item").removeClass("selected");
    $("#nav-create").addClass("selected");
    DashboardApp.events.trigger('showCreateView');
  },

  showRevive: function(e) {
    e.preventDefault();
    var links = $("#left-navbar").find(".list-group-item").removeClass("selected");
    $("#nav-revive").addClass("selected");
    DashboardApp.events.trigger('showReviveView');
  },

  showReview: function(e) {
    e.preventDefault();
    var links = $("#left-navbar").find(".list-group-item").removeClass("selected");
    $("#nav-review").addClass("selected");
    DashboardApp.events.trigger('showReviewView');
  },

  showActive: function(e) {
    e.preventDefault();
    var links = $("#left-navbar").find(".list-group-item").removeClass("selected");
    $("#nav-active").addClass("selected");
    DashboardApp.events.trigger('showActiveView');
  },

  onShow: function() {
    $("#nav-create").addClass("selected");
  }
});

DashboardApp.addInitializer(function(options) {
  var leftNavView = new DashboardApp.LeftNavView();
  DashboardApp.leftNavbarRegion.show(leftNavView);
});

/*
 * @author: Chris
 * @desc: a Marionette layout that wraps the left navbar, the dashboard
 *        proper and the modals. Expects to be intialized with a complete
 *        set of collections for every dashboard view. Handles navigation.
 */
DashboardApp.Layout = Backbone.Marionette.Layout.extend({
  template: "#layout-template",

  regions: {
    dashboard: '#dashboard'
  },

  initialize: function(options) {
    DashboardApp.events.on('showCreateView', this.showCreate, this);
    DashboardApp.events.on('showReviveView', this.showRevive, this);
    DashboardApp.events.on('showReviewView', this.showReview, this);
    DashboardApp.events.on('showActiveView', this.showActive, this);

    this.deals = options.deals;
    this.dealsFull = options.dealsFull;
    this.scheduledDeals = this.dealsFull.scheduledColl();
    this.expiredDeals = this.dealsFull.expiredColl();
    this.activeDealsCollectionView = new DealsCollectionView({
      collection: this.deals
    });
    this.scheduledDealsCollectionView = new DealsCollectionView({
      collection: this.scheduledDeals
    });
    this.expiredDealsCollectionView = new DealsCollectionView({
      collection: this.expiredDeals
    });
    this.dealCreateForm = new DealCreateFormView();
  },


  showCreate: function(e) {
    this.dashboard.show(this.dealCreateForm);
  },

  showRevive: function(e) {
    this.dashboard.show(this.expiredDealsCollectionView);
  },

  showReview: function(e) {
    this.dashboard.show(this.scheduledDealsCollectionView);
  },

  showActive: function(e) {
    this.dashboard.show(this.activeDealsCollectionView);
  },

  onShow: function() {
    this.dashboard.show(this.dealCreateForm);
  },
});

// Load the initializer
DashboardApp.addInitializer(function(options) {
  DashboardApp.events = _.extend({}, Backbone.Events);

  // Load all deals, pass them into a new layout
  var layoutOptions = {};
  layoutOptions.deals = new DealsCollection([], { 'vendorId': vendorId });
  layoutOptions.deals.fetch({ reset: true });
  layoutOptions.dealsFull = new FullDealsCollection([], { 'vendorId': vendorId});
  layoutOptions.dealsFull.fetch({ reset: true });

  var layout = new DashboardApp.Layout(layoutOptions);
  DashboardApp.dashboardRegion.show(layout);
});

$(document).ready(function() {
  DashboardApp.start();
});
