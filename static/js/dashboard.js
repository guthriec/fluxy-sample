// Start the dashboard Marionette/Backbone app
DashboardApp = new Backbone.Marionette.Application();

// Add regions of the DOM to the Marionette app for ease of manipulation
DashboardApp.addRegions({
  dealsRegion: '#deals',
  newDealFormRegion: '#new-deal-form'
});

/*
 * @author: Ayush, Chris
 * @desc: Defines the model that represents the deal that is going to be
 * displayed. 
 */

DealModel = Backbone.Model.extend({

  initialize: function(options) {
    if (options && options.id) {
      this.id = options.id;
    }
  },

  urlRoot: function() {
    if (this.collection) {
      vendorId = this.collection.vendorId || '-1';
      return '/api/v1/vendor/' + vendorId + '/deals/';
    }
    else {
      return '/api/v1/deals/';
    }
  }

});

/*
 * @author: Ayush
 * @desc: Defines the collection that represents a grouping of DealModel items.
 * Note: the defined URL is used as a GET request to get a list of deals to be
 * displayed.
 */
DealsCollection = Backbone.Collection.extend({

  model: DealModel,
  
  initialize: function(models, options) {
    this.vendorId = options.vendorId || -1;
  },

  url: function() {
    return '/api/v1/vendor/' + this.vendorId + '/deals/';
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
    var self=this;
    this.collection.create(newModel, {
      success: function(response) {
        console.log(self.collection);
        $('#submit-btn').blur();
      },
      error: function(err) {
        console.log(err);
      }
    }); 
  }
});

// Load the initializer
DashboardApp.addInitializer(function(options) {
  // Load all existing deals
  var deals = new DealsCollection([], { 'vendorId': '1' });
  deals.fetch({ reset: true });
  var dealsCollectionView = new DealsCollectionView({
    collection: deals
  });
  DashboardApp.dealsRegion.show(dealsCollectionView);

  // Load the form
  var dealCreateForm = new DealCreateFormView({
    collection: deals
  });
  DashboardApp.newDealFormRegion.show(dealCreateForm);
}); 

$(document).ready(function() {
  DashboardApp.start();
});
