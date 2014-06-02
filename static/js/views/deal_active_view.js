/*
 * @author: Chris
 * @desc: Defines the view that's responsible for rendering a single deal
 *        for Fluxy Live.
 */
define([
  'marionette',
  'fluxy_time',
  'vent'
], function(Marionette, FluxyTime, Vent) {
  var DealActiveView = Marionette.ItemView.extend({

    template: '#live-deal-template',
    
    tagName: 'tr',
    
    className: 'deal',
    
    serializeData: function() {
      var data = this.model.toJSON();
      var start_date = new Date(data.time_start);
      var end_date = new Date(data.time_end);
      data.pretty_time_start = FluxyTime.getDateStringHTML(start_date); 
      data.pretty_time_end = FluxyTime.getDateStringHTML(end_date);
      data.photo = data.photo.attributes;
      data.deals_claimed = 10;
      if (data.max_deals == -1) {
        data.deals_remaining = "Unlimited";
      } else {
        data.deals_remaining = data.max_deals - data.deals_claimed;
      }
      return data;
    }
  });
  return DealActiveView;
});
