DealCreateView = Backbone.View.extend({
  setVendor: function(vendorId) {
    this.vendorId = vendorId;
  },

  events: {
    'click .deal-form-submit' : 'postDeal' 
  },
  
  render: function() {
    this.$el.html(_.template($('#dealFormTemplate').html()));
    return this;
  },

  postDeal: function(e) {
    e.preventDefault();
    console.log("trying to post the deal");
    var dealModel = new VendorDealModel(this.vendorId);
    var $inputs = $('#deal-form :input');
    var values = {};
    $inputs.each(function() {
      values[this.name] = $(this).val();
    });
    dealModel.set("title", values["title"]);
    dealModel.set("desc", values["desc"]);
    dealModel.set("radius", 5);
    var timeStart = new Date()
    timeStart.setTime(Date.now());
    dealModel.set("time_start", timeStart); 
    var minutes = values["minutes"] + 60*values["hours"];
    dealModel.set("time_end", new Date(timeStart.getTime() + minutes*60000));
    console.log("posting...");
    console.log(dealModel);
    dealModel.save();
    var router = new DashboardRouter();
    router.navigate('view', {trigger: true}); 
  }
});
