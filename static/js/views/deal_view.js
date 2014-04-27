/*
 * @author: Ayush
 * @desc: Defines the view that is associated with the DealModel. It represents
 * a DealModel as a <tr> tag.
 */
define([
  'marionette',
], function(Marionette) {
  var DealView = Marionette.ItemView.extend({
    template: '#deal-template',
    tagName: 'tr',
    className: 'deal'
  });
  return DealView;
});
