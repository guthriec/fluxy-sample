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
DashboardApp.DealModel = Backbone.Model.extend({ });

/*
 * @author: Chris
 */
var SmartDealsSync = function(method, collection, options) {
  if (method=='read') {
    options.url = '/api/v1/vendor/' + collection.vendorId + '/deals/all/';
  } else {
    options.url = '/api/v1/vendor/' + collection.vendorId + '/deals/';
  }
  return Backbone.sync(method, collection, options);
}

/*
 * @author: Ayush, Chris
 * @desc: Defines the collection that represents a grouping of DealModel items.
 *        This collection also has functions scheduledColl and expiredColl that
 *        return DealsCollections filtered into scheduled and expired deals.
 *        These new collections listen to the original collection for changes
 *        and update themselves accordingly.
 */
DashboardApp.DealsCollection = Backbone.Collection.extend({

  model: DashboardApp.DealModel,

  sync: SmartDealsSync,

  initialize: function(models, options) {
    this.vendorId = options.vendorId || -1;
    this.url = '/api/v1/vendor/' + this.vendorId + '/deals/';
    if (options.listenForCreate == true) {
      DashboardApp.events.on('createDealTrigger', this.create, this);
    }
  },

  // Filter collection to include only deals that have not started.
  // Potential for web-iphone synchronization issues.
  scheduled: function() {
    return this.filter(function(deal) {
      return 0 < (new Date(deal.get('time_start') - Date.now()));
    });
  },

  // Returns collection that has only scheduled deals and updates whenever
  // the original DealsCollection gets updated.
  scheduledColl: function() {
    var filtered = this.scheduled();
    var scheduledCollection = new DashboardApp.DealsCollection(filtered, { 'vendorId': this.vendorId });
    var self = this;
    scheduledCollection.listenTo(self, 'add remove reset sync', function() {
      this.reset(self.scheduled(), { 'vendorId' : self.vendorId });
    });
    return scheduledCollection;
  },

  // Filter collection to include only deals that are active.
  // Potential for web-iphone synchronization issues.
  active: function() {
    return this.filter(function(deal) {
      return (0 > (new Date(deal.get('time_start') - Date.now())) && 0 < (new Date(deal.get('time_end')) - Date.now()));
    });
  },

  // Returns collection that has only scheduled deals and updates whenever
  // the original DealsCollection gets updated.
  activeColl: function() {
    var filtered = this.active();
    var activeCollection = new DashboardApp.DealsCollection(filtered, { 'vendorId': this.vendorId });
    var self = this;
    activeCollection.listenTo(self, 'add remove reset sync', function() {
      this.reset(self.active(), { 'vendorId' : self.vendorId });
    });
    return activeCollection;
  },

  // Filter collection to include only deals that have expired.
  // Pretends we're 1 minute in the future to mitigate synchronization issues.
  expired: function() {
    return this.select(function(deal) {
      return 0 > (new Date(deal.get('time_end')) - Date.now() - 60000);
    });
  },

  // Returns collection that has only expired deals and updates whenever
  // the original DealsCollection gets updated.
  expiredColl: function() {
    var filtered = this.expired();
    var expiredCollection = new DashboardApp.DealsCollection(filtered, { 'vendorId': this.vendorId });
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
DashboardApp.DealView = Backbone.Marionette.ItemView.extend({
  template: '#deal-template',
  tagName: 'tr',
  className: 'deal'
});

/*
 * @author: Ayush
 * @desc: Defines the view that is associated with DealsCollection. Is
 * responsible for showing all the DealView objects in a <table>.
 */
DashboardApp.DealsCollectionView = Backbone.Marionette.CompositeView.extend({
  tagname: 'table',
  id: 'deals-list-view',
  className: 'table table-striped table-bordered',
  template: '#deals-collection-template',
  itemView: DashboardApp.DealView,

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
    'click #create-deal-modal #create-btn': 'createDeal',
    'click #create-deal-modal #cancel-btn': 'cancelCreateDeal'
  },

  initialize: function() {
    DashboardApp.events.on('createDealConfirmTrigger', this.confirmDealCreation, this);
  },

  confirmDealCreation: function(deal) {
    this.newDeal = deal;

    var $modal = this.$el.find('#create-deal-modal');

    $modal.find('#title td:nth-child(2)').html(deal.title);
    $modal.find('#description td:nth-child(2)').html(deal.desc);

    var d = Math.abs((new Date(deal.time_start)) - (new Date(deal.time_end)));
    var hours = parseInt(d / 3600000);
    var minutes = d % 3600000 / 60000;
    $modal.find('#duration td:nth-child(2)').html(hours + 'H ' + minutes + 'M');

    $modal.modal('show');
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
DashboardApp.DealCreateFormView = Backbone.Marionette.ItemView.extend({
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
    this.scheduledDeals = this.deals.scheduledColl();
    this.expiredDeals = this.deals.expiredColl();
    this.activeDeals = this.deals.activeColl();
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
  // Load all deals, pass them into a new layout
  var layoutOptions = {};
  layoutOptions.deals= new DashboardApp.DealsCollection([], { 'vendorId': vendorId, 'listenForCreate': true });
  layoutOptions.deals.fetch({ reset: true });

  var layout = new DashboardApp.Layout(layoutOptions);
  DashboardApp.dashboardRegion.show(layout);
});

$(document).ready(function() {
  DashboardApp.start();
});
