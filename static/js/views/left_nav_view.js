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
      'click #nav-contact': 'showContact',
      'showCreateView': 'switchCreate',
      'showReviveView': 'switchRevive',
      'showReviewView': 'switchView',
      'showActiveView': 'switchActive',
    },

    showCreate: function(e) {
      e.preventDefault();
      vent.trigger('showCreateView');
    },

    switchCreate: function(e) {
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-create").addClass("selected");
    },

    showRevive: function(e) {
      e.preventDefault();
      vent.trigger('showReviveView');
    },

    switchRevive: function(e) {
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-revive").addClass("selected");
    },

    showReview: function(e) {
      e.preventDefault();
      vent.trigger('showReviewView');
    },

    switchReview: function(e) {
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-review").addClass("selected");
    },

    showActive: function(e) {
      e.preventDefault();
      vent.trigger('showActiveView');
    },

    switchActive: function(e) {
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-active").addClass("selected");
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
