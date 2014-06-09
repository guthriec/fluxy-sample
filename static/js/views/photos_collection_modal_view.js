/*
 * @author: Rahul
 * @desc: The view associated with the PhotosCollection. Manages new photo
 * uploading. Allows user to choose different photos.
 */
define([
  'jquery.form',
  'marionette',
  'views/photo_view',
  'vent',
], function(jqueryForm, Marionette, PhotoView, vent) {
  var PhotosCollectionModalView = Marionette.CompositeView.extend({
    template: '#photos-collection-modal-template',
    itemView: PhotoView,

    events: {
      'change #photo-input': 'postPhoto',
      'click .photos-modal-photo': 'choosePhoto'
    },

    collectionEvents: {
      'sync': 'render'
    },

    initialize: function() {
      vent.on('changePhotoTrigger', this.showPhotoModal, this);
    },

    postPhoto: function(e) {
      e.preventDefault();
      $('#upload-photo-form').ajaxSubmit({
        'success': function(context) {
          return function(res, status) {
            var photo = context.collection.add(res.data)[0];
            vent.trigger('photoChangedTrigger', photo);
            context.$el.find('#change-photo-modal').modal('hide');
          };
        }(this),
        'error': function() {
        }
      });
    },

    choosePhoto: function(e) {
      this.$el.find('#change-photo-modal').modal('hide');
    },

    showPhotoModal: function(deal) {
      this.$el.find('#change-photo-modal').modal('show');
    },

    appendHtml: function(collectionView, itemView) {
      collectionView.$('#photos-container').append(itemView.el);
    }
  });
  return PhotosCollectionModalView;
});
