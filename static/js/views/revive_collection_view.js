/*
 * @author: Chris 
 * @desc: The view that is associated with a collection of expired deals that
 * can be revived. Renders “no deals available” template if no expired deals.
 * Re-renders when the collection changes.
 */
define([
  'marionette',
  'views/deal_revive_view',
], function(Marionette, DealReviveView) {
  var ReviveCollectionView = Marionette.CompositeView.extend({
    id: 'revive-list-view',
    
    className: 'list-container',

    getTemplate: function() {
      if (this.collection.length == 0) {
        return "#empty-revive-template";
      } else {
        return "#revive-collection-template";
      }
    },

    itemView: DealReviveView,

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
  return ReviveCollectionView;
});
