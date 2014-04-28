/*
 * @author: Rahul
 * @desc: Defines the view associated with PhotosCollection.
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
      'change #photo-input': 'postPhoto'
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
            context.$el.find('#change-photo-modal').modal('hide');
          };
        }(this),
        'error': function() {
        }
      });
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
