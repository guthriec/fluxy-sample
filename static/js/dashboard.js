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
    'focusout #title-group' : 'validateTitleGroup',
    'focusout #duration-group' : function() {
      this.validateStart();
      this.validateDuration();
    },
    'focusout #start-time-group' : 'validateStart',
    'focusout #max-deals-group' : 'validateMaxDeals',
    'click #submit-btn': 'createDeal'
  },

  template: '#deal-create-form-template',

  /*
   * @author: Chris
   * @desc: Utility function to take the start-day-group and start-time-group
   *         elements, extract input, and compute the start time as a
   *         Javascript date.
   */
  computeStart: function(startDayEl, startTimeEl) {
    var dayInputEl = startDayEl.find('select[name="start-day"]');
    var hoursInputEl = startTimeEl.find('select[name="start-hours"]');
    var minutesInputEl = startTimeEl.find('select[name="start-minutes"]');
    var amPmInputEl = startTimeEl.find('select[name="start-am-pm"]');
    var timeStart = new Date();
    var startHours = Number(hoursInputEl.val());
    if(amPmInputEl.val() == 'pm') {
      startHours += 12;
    } else if(startHours == 12) {
      startHours = 0;
    }
    var startMinutes = Number(minutesInputEl.val()) + 60 * startHours;
    timeStart.setTime(Number(dayInputEl.val()) + 60000 * startMinutes);
    return timeStart;
  },

  /*
   * @author: Chris
   * @desc: Utility function to take the duration-group element, extract
   *        input, and compute the duration.
   */
  computeDuration: function(durationEl) {
    var minutesEl = durationEl.find('#duration-minutes');
    var hoursEl = durationEl.find('#duration-hours');
    return Number(minutesEl.val()) + 60 * Number(hoursEl.val());
  },

  /*
   * @author: Chris
   * @desc: Event handler to extract the input for start time,
   *        validate that the start time is after the current time, and update
   *        the form with appropriate errors.
   */
  validateStart: function(e) {
    var timeArea = this.$el.find('#time-area');
    var startDayEl = timeArea.find('#start-day-group');
    var startTimeEl = timeArea.find('#start-time-group');
    var startGroups = timeArea.find('#start-day-group').add('#start-time-group');
    var startTime = this.computeStart(startDayEl, startTimeEl);
    if (0 < (startTime - Date.now())) {
      startGroups.removeClass('has-error');
      this.$el.find('#start-validation-error').remove();
    } else {
      startGroups.addClass('has-error');
      if (this.$el.find('#start-validation-error').length == 0) {
        startTimeEl.append('<p id="start-validation-error" class="help-block col-sm-offset-2 col-sm-6">Start time must be in the future!</p>');
      }
    }
    this.events['change #start-day-group'] = 'validateStart';
    this.events['change #start-time-group'] = 'validateStart';
    delete this.events['focusout #start-am-pm'];
    this.delegateEvents();
  },

  /*
   * @author: Chris
   * @desc: Event handler to extract the input for deal title,
   *        validate that the title is long enough, and update
   *        the form with appropriate errors.
   */
  validateTitleGroup: function(e) {
    var titleEl = $('#title-group');
    var titleInputEl = titleEl.find('input:text[name="deal-title"]');
    var title = titleInputEl.val();
    if (title.length > 7) {
      titleEl.removeClass('has-error');
      this.$el.find('#title-validation-error').remove();
    } else {
      titleEl.addClass('has-error');
      var thirdChild= this.$el.find('#title-group :nth-child(3)');
      if (!(thirdChild.attr('id') == 'title-validation-error')) {
        thirdChild.before('<p id="title-validation-error" class="help-block col-sm-offset-2 col-sm-6">Deal title must be at least 8 characters long.</p>');
      }
    }
    this.events['keyup #title-group'] = 'validateTitleGroup';
    delete this.events['focusout #title-group'];
    this.delegateEvents();
  },

  /*
   * @author: Chris
   * @desc: Event handler to extract the input for duration,
   *        validate that duration is positive, and update
   *        the form with appropriate errors.
   */
  validateDuration: function(e) {
    var durationEl = this.$el.find('#duration-group');
    var duration = this.computeDuration(durationEl);
    if (duration > 0) {
      durationEl.removeClass('has-error');
      durationEl.find('#duration-validation-error').remove();
    } else {
      durationEl.addClass('has-error');
      var pEl= durationEl.find('p');
      if (!(pEl.attr('id') == 'duration-validation-error')) {
        pEl.before('<p id="duration-validation-error" class="help-block col-sm-offset-2 col-sm-6">Duration must be greater than 0</p>');
      }
    }
    this.events['change #duration-group'] = 'validateDuration';
    delete this.events['focusout #duration-group'];
    this.delegateEvents();
  },



  /*
   * @author: Chris
   * @desc: Event handler to extract the input for maximum number of deals,
   *        validate that this is a number between 1 and 500, and update
   *        the form with appropriate errors.
   */
  validateMaxDeals: function(e) {
    var maxDealsEl = this.$el.find('#max-deals-group');
    var maxDeals = parseInt(maxDealsEl.find('#max-deals-number').val(), 10);
    if (!isNaN(maxDeals) && maxDeals > 0 && maxDeals <= 500) {
      maxDealsEl.removeClass('has-error');
      this.$el.find('#max-deals-validation-error').remove();
    } else {
      maxDealsEl.addClass('has-error');
      if (this.$el.find('#max-deals-validation-error').length == 0) {
        maxDealsEl.append('<p id="max-deals-validation-error" class="help-block col-sm-6">Maximum number of deals must be a number between 1 and 500 (inclusive)</p>');
      }
    }
    this.events['keyup #max-deals-group'] = 'validateMaxDeals';
    delete this.events['focusout #max-deals-group'];
    this.delegateEvents();
  },

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
    var timeEnd = new Date();
    var timeStart = this.computeStart(this.$el.find('#start-day-group'), this.$el.find('#start-time-group'));
    var minutes = this.computeDuration(this.$el.find('#duration-group'));
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
