/*
 * @author: Ayush
 * @desc: Defines the view that is associated with DealsCollection. Is
 * responsible for showing all the DealView objects in a <table>.
 */
define([
  'jquery',
  'marionette',
  'views/deal_revive_view'
], function($, Marionette, DealReviveView) {
  var DealsCollectionView = Marionette.CompositeView.extend({
    tagname: 'table',
    id: 'deals-list-view',
    className: 'table table-striped table-bordered',
    template: '#revive-deals-collection-template',
    itemView: DealReviveView,

    collectionEvents: {
      "sync": "render"
    },

    appendHtml: function(collectionView, itemView) {
      collectionView.$('tbody').append(itemView.el);
    }
  });
  return DealsCollectionView;
});
