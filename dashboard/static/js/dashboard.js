DashboardApp = new Backbone.Marionette.Application();

DashboardApp.addRegions({
  dealsRegion: '#deals',
  newDealFormRegion: '#new-deal-form'
});

DealModel = Backbone.Model.extend({});
DealsCollection = Backbone.Collection.extend({
  model: DealModel,
  url: '/api/v1/vendor/1/deals'
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
    collectionView.$("tbody").append(itemView.el);
  }
});

DealCreateFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click .submit-btn': 'createDeal'
  },
  template: '#deal-create-form-template',
  render: function() {
    this.$el.html(_.template($(this.template).html()));
    console.log(this.$el);
    return this;
  },
  postDeal: function(e) {
    e.preventDefault();
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
