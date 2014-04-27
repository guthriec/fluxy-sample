/*
 * @author: Chris
 * RequireJS Main function for landing page
 */

require.config({
  paths: {
    jquery: 'lib/jquery-2.1.0.min',
  }
});

require(['analytics', 'csrf'], function(Analytics, Csrf) {
  Analytics.start();
  Csrf.start()
});
