/*
 * @author: Rahul
 * @desc: Defines the collection that represents the photos that belong to a
 * vendor.
 */
define([
  'backbone',
  'models/photo_model',
], function(Backbone, PhotoModel) {
  var PhotosCollection = Backbone.Collection.extend({

    model: PhotoModel,

    initialize: function(models, options) {
      this.vendorId = options.vendorId;
      this.url = '/api/v1/vendor/' + options.vendorId + '/photos/';
    },
  });
  return PhotosCollection;
});

