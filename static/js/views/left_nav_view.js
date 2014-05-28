define([
  'marionette',
  'vent'
], function(Marionette, vent) {
  var LeftNavView = Marionette.ItemView.extend({
    tagName: 'ul',
    className: 'nav nav-stacked list-group',
    id: 'left-navbar',
    template: '#left-navbar-template',

    events: {
      'click #nav-create': 'showCreate',
      'click #nav-revive': 'showRevive',
      'click #nav-review': 'showReview',
      'click #nav-active': 'showActive',
      'click #nav-contact': 'showContact'
    },

    showCreate: function(e) {
      e.preventDefault();
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-create").addClass("selected");
      vent.trigger('showCreateView');
    },

    showRevive: function(e) {
      e.preventDefault();
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-revive").addClass("selected");
      vent.trigger('showReviveView');
    },

    showReview: function(e) {
      e.preventDefault();
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-review").addClass("selected");
      vent.trigger('showReviewView');
    },

    showActive: function(e) {
      e.preventDefault();
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-active").addClass("selected");
      vent.trigger('showActiveView');
    },

    showContact: function(e) {
      e.preventDefault();
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-contact").addClass("selected");
      vent.trigger('showFeedbackView');
    },

    onShow: function() {
      $("#nav-create").addClass("selected");
    }
  });
  return LeftNavView;
});
