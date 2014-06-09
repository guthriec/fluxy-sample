VendorApp = new Backbone.Marionette.Application();

VendorApp.addRegions({
  vendorPhotoFormRegion: '#vendor-photo-form',
  vendorFormRegion: '#vendor-form'
});

VendorPhotoFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #save-photo-btn': 'postPhoto',
    'click #cancel-photo-btn': 'deletePhoto',
    'change #photo-src': 'changePhoto',
  },

  photo: null,

  template: '#vendor-photo-form-template',

  render: function() {
    this.$el.html(_.template($(this.template).html()));
    return this;
  },

  postPhoto: function(e) {
    e.preventDefault();
    $('#change-vendor-photo').modal('hide');
  },

  deletePhoto: function(e) {
    e.preventDefault();
    this.vendorId = this.vendorId || $('#photo-form').attr('data-vendor-id');
    if (this.photo)
      $.ajax('/api/v1/vendor/' + this.vendorId  + '/photo/' + this.photo.pk + '/',
          { 'type': 'delete' });
  },

  changePhoto: function(e) {
    $('#photo-form').ajaxSubmit({
      'success': function(context) {
        return function(res, status) {
          $('#modal-photo').attr('src', '/media/' + res[0].fields.photo);
          $('#save-photo-btn').removeClass('disabled');
          context.photo = res[0];
        };
      }(this),
      'error': function() {
      },
    });
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
