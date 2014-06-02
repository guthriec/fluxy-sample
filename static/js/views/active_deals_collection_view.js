/*
 * @author: Ayush
 * @desc: Defines the view that renders the Live collection. Is
 * responsible for showing all the DealLiveView objects.
 */
define([
  'marionette',
  'views/deal_live_view'
], function(Marionette, DealLiveView) {
  var LiveCollectionView = Marionette.CompositeView.extend({
    id: 'live-list-view',

    className: 'list-container',

    getTemplate: function() {
      if (this.collection.length == 0) {
        return "#empty-live-template";
      } else {
        return "#live-collection-template";
      }
    },

    itemView: DealLiveView,

    collectionEvents: {
      "all": "templateAndRender"
    },

    templateAndRender: function(e) {
      this.template = this.getTemplate();
      this.render();
    },

    appendHtml: function(collectionView, itemView) {
      collectionView.$('tbody').append(itemView.el);
    }
  });
  return LiveCollectionView;
});
