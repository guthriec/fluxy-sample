require.config({
  paths: {
    backbone: 'lib/backbone-1.1.2.min',
    'backbone.wreqr': 'lib/backbone.wreqr.min',
    bootstrap: 'lib/bootstrap.min',
    jquery: 'lib/jquery-2.1.0.min',
    marionette: 'lib/backbone.marionette.min',
    underscore: 'lib/underscore-1.6.0.min',
  },
  shim: {
    jquery: {
      exports: 'jQuery'
    },
    underscore: {
      exports: '_'
    },
    backbone: {
      deps: ['jquery', 'underscore'],
      exports: 'Backbone'
    },
    marionette: {
      deps: ['jquery', 'underscore', 'backbone'],
      exports: 'Marionette'
    },
  }
});

require(['dashboard'], function(DashboardApp) {
  console.log('starting the app');
  DashboardApp.start();
});
