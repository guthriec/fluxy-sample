// Start the dashboard Marionette/Backbone app
DashboardApp = new Backbone.Marionette.Application();

// Add regions of the DOM to the Marionette app for ease of manipulation
DashboardApp.addRegions({
  dealsRegion: '#deals',
  newDealFormRegion: '#new-deal-form'
});

/*
 * @author: Ayush
 * @desc: Defines the model that represents the deal that is going to be
 * displayed. Note: the defined URL is used for a POST request when a new deal
 * is created.
 */
DealModel = Backbone.Model.extend({
  url: '/api/v1/vendor/1/deals/'
});

/*
 * @author: Ayush
 * @desc: Defines the collection that represents a grouping of DealModel items.
 * Note: the defined URL is used as a GET request to get a list of deals to be
 * displayed.
 */
DealsCollection = Backbone.Collection.extend({
  model: DealModel,
  // TODO: dynamiv vendor ID
  url: '/api/v1/vendor/1/deals/'
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
  className: 'table-striped table-bordered',
  template: '#deals-collection-template',
  itemView: DealView,

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
    'click .submit-btn': 'createDeal'
  },
  template: '#deal-create-form-template',

  render: function() {
    this.$el.html(_.template($(this.template).html()));
    return this;
  },

  createDeal: function(e) {
    e.preventDefault();

    var newModel = new DealModel();

    var $formInputs = $('#deal-form :input');
    var formValues = {};
    $formInputs.each(function() {
      formValues[this.name] = $(this).val();
    });
    newModel.set('title', formValues['title']);
    newModel.set('desc', formValues['desc']);
    var timeStart = (new Date()).toUTCString();
    newModel.set('time_start', timeStart);
    var minutes = formValues['minutes'] + 60 * formValues['hours'];
    var timeEnd = (new Date(Date.now() + minutes * 60000).toUTCString())
    newModel.set('time_end', timeEnd);
    newModel.save(); 
  }
});

// Load the initializer
DashboardApp.addInitializer(function(options) {
  // Load all existing deals
  var deals = new DealsCollection();
  deals.fetch({ reset: true });
  var dealsCollectionView = new DealsCollectionView({
    collection: deals
  });
  DashboardApp.dealsRegion.show(dealsCollectionView);

  // Load the form
  var dealCreateForm = new DealCreateFormView();
  DashboardApp.newDealFormRegion.show(dealCreateForm);
}); 

$(document).ready(function() {
  DashboardApp.start();
});