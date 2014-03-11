DashboardApp = new Backbone.Marionette.Application();

DashboardApp.addRegions({
  dealsRegion: '#deals',
  newDealFormRegion: '#new-deal-form'
});

DealModel = Backbone.Model.extend({
  url: '/api/v1/vendor/1/deals/'
});
DealsCollection = Backbone.Collection.extend({
  model: DealModel,
  // TODO: dynamiv vendor ID
  url: '/api/v1/vendor/1/deals/'
});

DealView = Backbone.Marionette.ItemView.extend({
  template: '#deal-template',
  tagName: 'tr',
  className: 'deal'
});
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
    // TODO dynamic vendor ID
    newModel.set('vendorId', 1);
    newModel.set('title', formValues['title']);
    newModel.set('desc', formValues['desc']);
    newModel.set('radius', 5);
    var timeStart = new Date().setTime(Date.now());
    newModel.set('time_start', timeStart);
    var minutes = formValues['minutes'] + 60 * formValues['hours'];
    newModel.set('time_end', (new Date(Date.now() + minutes * 60000)));
    newModel.save(); 
  }
});

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
