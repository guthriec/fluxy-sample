VendorApp = new Backbone.Marionette.Application();

VendorApp.addRegions({
  vendorFormRegion: '#vendor-form'
});

VendorModel = Backbone.Model.extend({ });

VendorFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #submit-btn': 'editDeal'
  },
  template: "#vendor-edit-form-template",

  render: function() {
    this.$el.html(_.template($(this.template).html()));
    return this;
  },

  editDeal: function(e) {
    e.preventDefault();

    var $formInputs = $('#vendor-form :input');
    var formValues = {};
    $formInputs.each(function() {
      formValues[this.name] = $(this).val();
    });

    console.log(formValues);
    $.ajax({
      url: '/api/v1/vendor/1/',
      type: 'PUT',
      contentType: 'application/json',
      data: JSON.stringify(formValues)
    });
    this.$el.find('#submit-btn').blur();
  }
});

VendorApp.addInitializer(function(options) {
  VendorApp.events = _.extend({}, Backbone.Events);

  var vendorForm = new VendorFormView();
  VendorApp.vendorFormRegion.show(vendorForm);
});

$(document).ready(function() {
  VendorApp.start();
});
