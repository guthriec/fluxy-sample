var app = app || {};

(function() {
  app.AuthModel = Backbone.Model.extend({
    url: "/api/v1/auth/"
  });
})();
