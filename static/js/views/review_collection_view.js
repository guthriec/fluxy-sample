/*
 * @author: Chris 
 * @desc: Defines the view that is associated with a collection of 
 * scheduled deals for review. Is responsible for showing all the DealView
 * objects in a <table>.
 */
define([
  'marionette',
  'views/deal_review_view',
], function(Marionette, DealReviewView) {
  var ReviewCollectionView = Marionette.CompositeView.extend({
    id: 'review-list-view',
    
    className: 'list-container',

    getTemplate: function() {
      if (this.collection.length == 0) {
        return "#empty-review-template";
      } else {
        return "#review-collection-template";
      }
    },

    itemView: DealReviewView,

    /* An issue that needs to be resolved eventually: Template and render is
     * being called 2-3 times each time the tab gets opened or a deal gets
     * cancelled. I think this is due to us being overgenerous in which events
     * we are listening to. */
    collectionEvents: {
      'all': 'templateAndRender',
    },

    templateAndRender: function(e) {
      this.template = this.getTemplate();
      this.render();
    },

    onRender: function() {
      this.delegateEvents();
    },

    appendHtml: function(collectionView, itemView) {
      collectionView.$('tbody').append(itemView.el);
    }
  });
  return ReviewCollectionView;
});
