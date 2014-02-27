var DealsListView = Backbone.View.extend({
  initialize: function() {
    this.deals = DealCollection.fetch();
  },

  render: function() {
    template = _.template($('#dealsListTemplate'));
    this.$el.html(template);
    return this;
  }
});
