VendorApp = new Backbone.Marionette.Application();

VendorApp.addRegions({
  vendorPhotoFormRegion: '#vendor-photo-form',
  vendorFormRegion: '#vendor-form'
});

VendorPhotoFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #save-picture-btn': 'postPhoto',
    'change #photo-src': 'changePhoto',
  },

  template: '#vendor-photo-form-template',

  render: function() {
    this.$el.html(_.template($(this.template).html()));
    return this;
  },

  postPhoto: function(e) {
    e.preventDefault();
    $('#photo-form').ajaxSubmit({
      'success': function(res, status) {
        $('#vendor-image').attr('src', '/media/' +
          JSON.parse(res)[0].fields.image);
        $('#change-vendor-photo').modal('hide');
      },
      'error': function() {
      },
    });
  },

  changePhoto: function(e) {
    $('#save-picture-btn').removeClass('disabled');
  }
});

VendorFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #submit-btn': 'editVendor',
  },
  template: "#vendor-edit-form-template",

  render: function() {
    this.$el.html(_.template($(this.template).html()));
    return this;
  },

  editVendor: function(e) {
    e.preventDefault();

    $('#vendor-attrs-form').ajaxSubmit({
      'success': function(res, status) {
      },
      'error': function() {
      },
    });

    this.$el.find('#submit-btn').blur();
  },
});

VendorApp.addInitializer(function(options) {
  VendorApp.events = _.extend({}, Backbone.Events);

  var vendorPhotoForm = new VendorPhotoFormView();
  VendorApp.vendorPhotoFormRegion.show(vendorPhotoForm);
  var vendorForm = new VendorFormView();
  VendorApp.vendorFormRegion.show(vendorForm);
});

$(document).ready(function() {
  VendorApp.start();
});
