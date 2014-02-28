var DealsListView = Backbone.View.extend({
  initialize: function() {
    vd_collection = new VendorDealCollection();
    vd_collection.set_vendor(1);
    this.deals = vd_collection.fetch();
    console.log(this.deals);
  },

  render: function() {
    template = _.template($('#dealsListTemplate').html());
    this.$el.html(template);
    return this;
  }
});
