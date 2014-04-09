// Start the dashboard Marionette/Backbone app
DashboardApp = new Backbone.Marionette.Application();

// Add regions of the DOM to the Marionette app for ease of manipulation
DashboardApp.addRegions({
  activeDealsRegion: '#active-deals',
  scheduledDealsRegion: '#scheduled-deals',
  expiredDealsRegion: '#expired-deals',
  newDealFormRegion: '#new-deal-form',
  modalControllerViewRegion: '#modals'
});

/*
 * @author: Ayush, Chris
 * @desc: Defines the model that represents the deal that is going to be
 * displayed. 
 */
DealModel = Backbone.Model.extend({ });

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
 * @desc: Same as DealsCollection, but hooks into the /vendor/deals/all endpoint
 * TODO: factor
 */

FullDealsCollection = Backbone.Collection.extend({

  model: DealModel,
  
  initialize: DealCollInit,

  url: function() {
    return '/api/v1/vendor/' + this.vendorId + '/deals/all/';
  },

  scheduled: function() {
    return this.filter(function(deal) {
      return 0 < (new Date(deal.get('time_start') - Date.now() - 60000));
    });
  },

  scheduledColl: function() {
    var filtered = this.scheduled();
    var scheduledCollection = new FullDealsCollection(filtered, { 'vendorId': this.vendorId });
    var self = this;
    scheduledCollection.listenTo(self, 'add remove reset sync', function() {
      this.reset(self.scheduled(), { 'vendorId' : self.vendorId });
    });
    return scheduledCollection;
  },

  expired: function() {
    return this.select(function(deal) {
      return 0 > (new Date(deal.get('time_end')) - Date.now() + 60000);
    });
  },
  
  expiredColl: function() {
    var filtered = this.expired();
    var expiredCollection = new FullDealsCollection(filtered, { 'vendorId': this.vendorId });
    var self = this;
    expiredCollection.listenTo(self, 'add remove reset sync', function() {
      console.log('poooop');
      console.log(self.expired());
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
 * @desc: Responsible for rendering and displaying any necessary modals 
 */
ModalControllerView = Backbone.Marionette.ItemView.extend({
  template: '#modal-controller-template',

  events: {
    'click #confirm-create-deal-modal #create-btn': 'createDeal',
    'click #confirm-create-deal-modal #cancel-btn': 'cancelCreateDeal'
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
DealCreateFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #submit-btn': 'createDeal'
  },
  template: '#deal-create-form-template',

  render: function() {
    this.$el.html(_.template($(this.template).html()));

    // Set up the JQuery UI Spinners
    this.$el.find('#hours').spinner({
      spin: function(event, ui) {
        if(ui.value >= 5) {
          $(this).spinner('value', 5);
          return false;
        } else if (ui.value < 0) {
          $(this).spinner('value', 0);
          return false;
        }
      }
    });
    this.$el.find('#minutes').spinner({
      spin: function(event, ui) {
        if (ui.value >= 60) {
          $(this).spinner('value', 60);
          return false;
        } else if (ui.value < 0) {
          $(this).spinner('value', 0);
          return false;
        }
      }
    });
    return this;
  },

  createDeal: function(e) {
    e.preventDefault();

    var newModel = {};

    var $formInputs = $('#deal-form :input');
    var formValues = {};
    $formInputs.each(function() {
      formValues[this.name] = $(this).val();
    });
    newModel['title'] = formValues['title'];
    newModel['desc'] = formValues['desc'];
    var timeStart = (new Date()).toUTCString();
    newModel['time_start'] = timeStart;
    var minutes = Number(formValues['minutes']) + 60 * formValues['hours'];
    var timeEnd = (new Date(Date.now() + minutes * 60000).toUTCString())
    newModel['time_end'] = timeEnd;
    newModel['max_deals'] = 0;
    newModel['instructions'] = 'Show to waiter';

    DashboardApp.events.trigger('createDealConfirmTrigger', newModel);
    this.$el.find('#submit-btn').blur();
  }
});

// Load the initializer
DashboardApp.addInitializer(function(options) {
  DashboardApp.events = _.extend({}, Backbone.Events);

  // Load all existing deals
  var deals = new DealsCollection([], { 'vendorId': vendorId });
  deals.fetch({ reset: true });
  var dealsFull = new FullDealsCollection([], { 'vendorId': vendorId});
  dealsFull.fetch({ reset: true });
  var scheduledDeals = dealsFull.scheduledColl();
  var expiredDeals = dealsFull.expiredColl();
  console.log(dealsFull);
  var dealsCollectionView = new DealsCollectionView({
    collection: deals
  });
  DashboardApp.activeDealsRegion.show(dealsCollectionView);

  var scheduledDealsCollectionView = new DealsCollectionView({
    collection: scheduledDeals 
  });
  
  DashboardApp.scheduledDealsRegion.show(scheduledDealsCollectionView);

  var expiredDealsCollectionView = new DealsCollectionView({
    collection: expiredDeals
  });

  DashboardApp.expiredDealsRegion.show(expiredDealsCollectionView);

  // Load the form
  var dealCreateForm = new DealCreateFormView();
  DashboardApp.newDealFormRegion.show(dealCreateForm);
}); 

DashboardApp.addInitializer(function(options) {
  var modalControllerView = new ModalControllerView();
  DashboardApp.modalControllerViewRegion.show(modalControllerView);
});

$(document).ready(function() {
  DashboardApp.start();
});
