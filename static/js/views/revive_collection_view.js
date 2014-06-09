/*
 * @author: Chris 
 * @desc: Defines the view that is associated with a collection of 
 * expired deals. Is responsible for showing all the DealView
 * objects in a <table>.
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