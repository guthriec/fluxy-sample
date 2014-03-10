DashboardApp = new Backbone.Marionette.Application();

DashboardApp.addRegions({
  dealsRegion: '#deals'
});

DealModel = Backbone.Model.extend({});
DealsCollection = Backbone.Collection.extend({
  model: DealModel
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

DashboardApp.addInitializer(function(options) {
  var dealsCollectionView = new DealsCollectionView({
    collection: options.deals
  });
  DashboardApp.dealsRegion.show(dealsCollectionView);
}); 

$(document).ready(function() {
  var deals = new DealsCollection([
    new DealModel({ title: 'Deal1' }),
    new DealModel({ title: 'Deal2' }),
    new DealModel({ title: 'Deal3' })
  ]);

  DashboardApp.start({ deals: deals });
});
