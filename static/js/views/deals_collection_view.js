/*
 * @author: Ayush
 * @desc: Defines the view that is associated with DealsCollection. Is
 * responsible for showing all the DealView objects in a <table>.
 */
define([
  'marionette',
  'views/deal_view'
], function(Marionette, DealView) {
  var DealsCollectionView = Marionette.CompositeView.extend({
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
  return DealsCollectionView;
});
