/*
 * @author: Chris
 * I didn't test this but it should be a good main function for 
 */

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
    bootstrap: {
      deps: ['jquery']
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

require(['analytics', 'csrf'], function(Analytics, Csrf) {
  Analytics.start();
  Csrf.start()
});
