<<<<<<< HEAD
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

DashboardApp.PhotoModel = Backbone.Model.extend({ });

DashboardApp.PhotosCollection = Backbone.Collection.extend({

  initialize: function(models, options) {
    this.vendorId = options.vendorId;
    this.url = '/api/v1/vendor/' + options.vendorId + '/photos/';
  },

});

/*
 * @author: Ayush, Chris
 * @desc: Defines the collection that represents a grouping of DealModel items.
 *        This collection also has functions scheduledCollection and
 *        expiredCollection that return DealsCollections filtered into
 *        scheduled and expired deals. These new collections listen to the
 *        original collection for changes and update themselves accordingly.
 */
DashboardApp.DealsCollection = Backbone.Collection.extend({

  model: DashboardApp.DealModel,

  sync: function(method, collection, options) {
    if(method=='read') {
      options.url = '/api/v1/vendor/' + collection.vendorId + '/deals/all/';
    } else {
      options.url = '/api/v1/vendor/' + collection.vendorId + '/deals/';
    }
    return Backbone.sync(method, collection, options);
  },

  initialize: function(models, options) {
    this.vendorId = options.vendorId || -1;
    this.url = '/api/v1/vendor/' + this.vendorId + '/deals/';
    if(options.listenForCreate == true) {
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
  scheduledCollection: function() {
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
  activeCollection: function() {
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
  expiredCollection: function() {
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
 * @author: Rahul
 * @desc: Defines the view associated with the PhotoModel.
 */
DashboardApp.PhotoView = Backbone.Marionette.ItemView.extend({
  template: '#photo-template',
});

DashboardApp.PhotosCollectionModalView = Backbone.Marionette.CompositeView.extend({
  template: '#photos-collection-modal-template',
  itemView: DashboardApp.PhotoView,

  collectionEvents: {
    'sync': 'render'
  },

  initialize: function() {
    DashboardApp.events.on('changePhotoTrigger', this.showPhotoModal, this);
  },

  showPhotoModal: function(deal) {
    this.$el.find('#change-photo-modal').modal('show');
  },

  appendHtml: function(collectionView, itemView) {
    collectionView.$('#photos-modal-content').append(itemView.el);
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
 * @desc: Responsible for rendering and displaying deal creation modals.
 */
DashboardApp.DealCreateModalView = Backbone.Marionette.ItemView.extend({
  template: '#deal-create-modal-template',

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

/*
 * @author: Ayush
 * @desc: Defines the view that is associated with the form that allows vendors
 * to create a new deal. It is responsible for handling all events associated
 * with the form.
 */
DashboardApp.DealCreateFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #change-photo-btn': 'changePhoto',
    'click #submit-btn': 'createDeal'
  },
  template: '#deal-create-form-template',

  render: function() {
    this.$el.html(_.template($(this.template).html()));

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
        if($(this).is(':checked') && (this).value == 'limited') {
          $('#max-deals-number').prop('disabled', false);
          $('#max-deals-number').attr('placeholder', '1  --  500');
          $('#max-deals-number').attr('maxlength', '3');
        }
        if($(this).is(':checked') && (this).value == 'unlimited') {
          $('#max-deals-number').prop('disabled', true);
          $('#max-deals-number').attr('placeholder', 'Unlimited');
          $('#max-deals-number').val('');
        }
      }
    );
    return this;
  },

  changePhoto: function(e) {
    DashboardApp.events.trigger('changePhotoTrigger', {});
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
    if(formValues['start-am-pm'] == 'pm') {
      startHours += 12;
    } else if(startHours == 12) {
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
    if(limitRadio.is(':checked')) {
      newModel['max_deals'] = Number(formValues['max-deals']);
    }
    newModel['instructions'] = 'Show to waiter';
    DashboardApp.events.trigger('createDealConfirmTrigger', newModel);
    this.$el.find('#submit-btn').blur();
  }
});

DashboardApp.ProfileEditFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #save-photo-btn': 'postPhoto',
    'click #cancel-photo-btn': 'deletePhoto',
    'change #photo-src': 'changePhoto',
  },

  photo: null,

  template: '#profile-photo-form-template',

  render: function() {
    this.$el.html(_.template($(this.template).html()));
    return this;
  },

  postPhoto: function(e) {
    e.preventDefault();
    $('#change-vendor-photo').modal('hide');
  },

  deletePhoto: function(e) {
    e.preventDefault();
    this.vendorId = this.vendorId || $('#photo-form').attr('data-vendor-id');
    if (this.photo)
      $.ajax('/api/v1/vendor/' + this.vendorId  + '/photo/' + this.photo.pk + '/',
          { 'type': 'delete' });
  },

  changePhoto: function(e) {
    $('#photo-form').ajaxSubmit({
      'success': function(context) {
        return function(res, status) {
          // $('#modal-photo').attr('src', '/media/' + res[0].fields.photo);
          $('#save-photo-btn').removeClass('disabled');
          context.photo = res[0];
        };
      }(this),
      'error': function() {
      },
    });
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
    'click #nav-active': 'showActive',
    'click #nav-profile': 'showProfile',
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

  showProfile: function(e) {
    e.preventDefault();
    var links = $("#left-navbar").find(".list-group-item").removeClass("selected");
    $("#nav-profile").addClass("selected");
    DashboardApp.events.trigger('showProfileView');
  },

  onShow: function() {
    $("#nav-create").addClass("selected");
  }
});

DashboardApp.addInitializer(function(options) {
  var leftNavView = new DashboardApp.LeftNavView();
  DashboardApp.leftNavbarRegion.show(leftNavView);
});

DashboardApp.ModalContent = Backbone.Marionette.Layout.extend({
  template: '#modal-content-template',

  regions: {
    modal: '#modal'
  },

  initialize: function(options) {
    DashboardApp.events.on('createDealConfirmTrigger', this.confirmCreate, this);
    DashboardApp.events.on('changePhotoTrigger', this.changePhoto, this);

    this.dealCreateModalView = new DashboardApp.DealCreateModalView();
    this.photos = options.photos;
    this.photosCollectionModalView = new DashboardApp.PhotosCollectionModalView({
      collection: this.photos
    });
  },

  confirmCreate: function() {
    this.modal.show(this.dealCreateModalView);
  },

  changePhoto: function() {
    this.modal.show(this.photosCollectionModalView);
  }
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
  var mainOpts = {};
  mainOpts.deals = new DashboardApp.DealsCollection([], { 'vendorId': vendorId, 'listenForCreate': true });
  mainOpts.deals.fetch({ reset: true });

  mainOpts.vendors = new DashboardApp.VendorsCollection([], { });
  mainOpts.vendors.fetch({ reset: true });

  var mainContent = new DashboardApp.MainContent(mainOpts);
  DashboardApp.dashboardRegion.show(mainContent);

  var modalOpts = {};
  modalOpts.photos = new DashboardApp.PhotosCollection([], { 'vendorId': vendorId });
  modalOpts.photos.fetch({ reset: true });

  var modalContent = new DashboardApp.ModalContent(modalOpts);
  DashboardApp.modalRegion.show(modalContent);
});

$(document).ready(function() {
  DashboardApp.start();
=======
define([
  'backbone',
  'marionette',
  'underscore',
  'views/modal_controller_view',
  'views/left_nav_view',
  'collections/deals_collection',
  'layouts/main_content_layout'
], function(Backbone, Marionette, _, ModalControllerView, LeftNavView,
            DealsCollection, MainContentLayout) {

  // Start the dashboard Marionette/Backbone app
  var DashboardApp = new Marionette.Application();

  // Register the main dashboard region
  DashboardApp.addRegions({
    dashboardRegion: '#dashboard-container',
    leftNavbarRegion: '#left-navbar-container',
    modalRegion: '#modal-container'
  }),

  DashboardApp.addInitializer(function(options) {
    var modalControllerView = new ModalControllerView();
    DashboardApp.modalRegion.show(modalControllerView);
  });

  DashboardApp.addInitializer(function(options) {
    var leftNavView = new LeftNavView();
    DashboardApp.leftNavbarRegion.show(leftNavView);
  });

  // Load the initializer
  DashboardApp.addInitializer(function(options) {
    var opts = {};
    opts.deals = new DealsCollection([], { 'vendorId': vendorId,
                                           'listenForCreate': true });
    opts.deals.fetch({ reset: true });

    var mainContent = new MainContentLayout(opts);
    DashboardApp.dashboardRegion.show(mainContent);
  });

  return DashboardApp;
>>>>>>> dev
});
