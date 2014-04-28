/*
 * @author: Rahul
 * @desc: Defines the view associated with PhotosCollection.
 */
define([
  'marionette',
  'views/photo_view',
  'vent'
], function(Marionette, PhotoView, vent) {
  var PhotosCollectionModalView = Marionette.CompositeView.extend({
    template: '#photos-collection-modal-template',
    itemView: PhotoView,

    collectionEvents: {
      'sync': 'render'
    },

    initialize: function() {
      vent.on('changePhotoTrigger', this.showPhotoModal, this);
    },

    showPhotoModal: function(deal) {
      this.$el.find('#change-photo-modal').modal('show');
    },

    appendHtml: function(collectionView, itemView) {
      collectionView.$('#photos-modal-content').append(itemView.el);
    }
  });
  return PhotosCollectionModalView;
});
