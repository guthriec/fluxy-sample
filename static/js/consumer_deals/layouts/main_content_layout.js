/*
 * @author: Chris
 * @desc: a Marionette layout that wraps the main content of the deals view.
 */
define([
  'marionette',
  'vent'
], function(Marionette, vent) { 
  var MainContentLayout = Marionette.Layout.extend({
    template: "#main-content-template",

    regions: {
      dealsRegion: '#deals'
    },

    initialize: function(options) {
      this.deals = options.deals;
    },
  });
  return MainContentLayout;
});
