var DealsListView = Backbone.View.extend({
  initialize: function() {
    var vd_collection = new VendorDealCollection();
    vd_collection.set_vendor(1);
    vd_collection.fetch({
      success: function() {
        console.log(vd_collection)
        console.log(vd_collection.models)
        console.log(vd_collection.models[0]);
      }
    });
  },

  render: function() {
    template = _.template($('#dealsListTemplate').html());
    this.$el.html(template);
    return this;
  }
});
