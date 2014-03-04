var app = app || {};

(function() {
  app.AuthModel = Backbone.Model.extend({
    url: "/user/auth/"
  });
})();
