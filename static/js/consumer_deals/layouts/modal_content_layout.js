/*
 * @author: Chris
 * @desc: A Marionette layout that wraps the modal content of the deals view.
 * Initializes the modals.
 */
define([
  'marionette',
  'vent'
], function(Marionette, vent) {
  var ModalContentLayout = Marionette.Layout.extend({
    template: '#modal-content-template',

    regions: {
      modal: '#modal'
    }
  });
  return ModalContentLayout;
});
