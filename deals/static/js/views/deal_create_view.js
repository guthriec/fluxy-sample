DealCreateView = Backbone.View.extend({
  events: {
    // on submit
  },
  render: function() {
    this.$el.html(_.template($('#dealFormTemplate').html()));
    return this;
  }
});
