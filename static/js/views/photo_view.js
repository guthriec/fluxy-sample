/*
 * @author: Rahul
 * @desc: Defines the view associated with the PhotoModel. Includes
 * functionality for choosing a photo for a new deal.
 */
define([
  'marionette',
  'vent'
], function(Marionette, vent) {
  var PhotoView = Marionette.ItemView.extend({
    template: '#photo-template',

    events: {
      'click': 'choose'
    },

    /*
     * @author: Rahul
     * @desc: Triggers the deal creation form to display the selected photo.
     */
    choose: function(e) {
      vent.trigger('photoChangedTrigger', this.model);
    }
  });
  return PhotoView;
});
