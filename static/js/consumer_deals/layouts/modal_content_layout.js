/*
 * @author: Rahul
 * @desc: A Marionette layout that wraps the modal content of the dashboard.
 * Initializes the modals, and on appropriate triggers, shows the deal
 * confirmation modal or the photo selection modal.
 */
define([
  'marionette',
  'vent',
  'views/deal_create_modal_view',
  'views/photos_collection_modal_view'
], function(Marionette, vent, DealCreateModalView, PhotosCollectionModalView) {
  var ModalContentLayout = Marionette.Layout.extend({
    template: '#modal-content-template',

    regions: {
      modal: '#modal'
    },

    initialize: function(options) {
      vent.on('createDealConfirmTrigger', this.confirmCreate, this);
      vent.on('changePhotoTrigger', this.changePhoto, this);

      this.dealCreateModalView = new DealCreateModalView();
      this.photos = options.photos;
      this.photosCollectionModalView = new PhotosCollectionModalView({
        collection: this.photos
      });
    },

    confirmCreate: function() {
      this.modal.show(this.dealCreateModalView);
    },

    changePhoto: function() {
      this.modal.show(this.photosCollectionModalView);
    }
  });
  return ModalContentLayout;
});
