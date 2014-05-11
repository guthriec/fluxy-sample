/*
 * @author: Chris 
 * @desc: Defines the view that is associated with a collection of 
 * scheduled deals for review. Is
 * responsible for showing all the DealView objects in a <table>.
 */
define([
  'marionette',
  'views/deal_review_view',
], function(Marionette, DealReviewView) {
  var ReviewCollectionView = Marionette.CompositeView.extend({
    tagname: 'table',
    id: 'review-list-view',
    className: 'table table-striped table-bordered',

    getTemplate: function() {
      if (this.collection.length == 0) {
        return "#empty-review-template";
      } else {
        return "#review-collection-template";
      }
    },

    itemView: DealReviewView,

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
  return ReviewCollectionView;
});
