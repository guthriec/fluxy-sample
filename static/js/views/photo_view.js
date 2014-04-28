/*
 * @author: Rahul
 * @desc: Defines the view associated with the PhotoModel.
 */
define([
  'marionette',
], function(Marionette) {
  var PhotoView = Marionette.ItemView.extend({
    template: '#photo-template',
  });
  return PhotoView;
});
