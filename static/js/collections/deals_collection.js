/*
 * @author: Ayush, Chris
 * @desc: Defines the collection that represents a grouping of DealModel items.
 *        This collection also has functions scheduledCollection and 
 *        expiredCollection that return DealsCollections filtered into 
 *        scheduled and expired deals. These new collections listen to the 
 *        original collection for changes and update themselves accordingly.
 */
define([
  'backbone',
  'models/deal_model',
  'vent'
], function(Backbone, DealModel, vent) {
  var DealsCollection = Backbone.Collection.extend({

    model: DealModel,

    sync: function(method, collection, options) {
      if(method=='read') {
        options.url = '/api/v1/vendor/' + collection.vendorId + '/deals/all/';
      } else {
        options.url = '/api/v1/vendor/' + collection.vendorId + '/deals/';
      }
      return Backbone.sync(method, collection, options);
    },

    initialize: function(models, options) {
      this.vendorId = options.vendorId || -1;
      this.url = '/api/v1/vendor/' + this.vendorId + '/deals/';
      if(options.listenForChanges == true) {
        vent.on('createDealTrigger', this.createAndFetch, this);
        vent.on('cancelDealTrigger', this.cancelAndFetch, this);
      }
    },

    createAndFetch: function(model) {
      var self = this;
      this.create(model, {
        wait: true,
        success: function(resp) {
          console.log('deal created - refreshing collection');
          self.fetch(); 
        }
      });
    },

    cancelAndFetch: function(model) {
      var self = this;
      model.destroy({
        wait: true,
        success: function(model, response) {
          console.log('deal cancelled - refreshing collection');
          self.fetch();
        }
      }); 
      this.fetch();
    },

    // Filter collection to include only deals that have not started.
    // Potential for web-iphone synchronization issues.
    scheduled: function() {
      return this.filter(function(deal) {
        return (deal.get('stage') == 0); 
      });
    },

    // Returns collection that has only scheduled deals and updates whenever
    // the original DealsCollection gets updated.
    scheduledCollection: function() {
      var filtered = this.scheduled();
      var scheduledCollection = new DealsCollection(filtered, 
                                                    { 'vendorId': 
                                                      this.vendorId });
      var self = this;
      scheduledCollection.listenTo(self, 'reset sync', function() {
        this.reset(self.scheduled(), { 'vendorId' : self.vendorId });
      });
      return scheduledCollection;
    },

    // Filter collection to include only deals that are active.
    // Potential for web-iphone synchronization issues.
    active: function() {
      return this.filter(function(deal) {
        return (0 > (new Date(deal.get('time_start') - Date.now())) && 
                0 < (new Date(deal.get('time_end')) - Date.now()));
      });
    },

    // Returns collection that has only scheduled deals and updates whenever
    // the original DealsCollection gets updated.
    activeCollection: function() {
      var filtered = this.active();
      var activeCollection = new DealsCollection(filtered, 
                                                 { 'vendorId': this.vendorId });
      var self = this;
      activeCollection.listenTo(self, 'all', function() {
        this.reset(self.active(), { 'vendorId' : self.vendorId });
      });
      return activeCollection;
    },

    // Filter collection to include only deals that have expired.
    // Pretends we're 1 minute in the future to mitigate synchronization issues.
    expired: function() {
      return this.select(function(deal) {
        return 0 > (new Date(deal.get('time_end')) - Date.now() - 60000);
      });
    },

    // Returns collection that has only expired deals and updates whenever
    // the original DealsCollection gets updated.
    expiredCollection: function() {
      var filtered = this.expired();
      var expiredCollection = new DealsCollection(filtered, 
                                                  { 'vendorId':
                                                    this.vendorId });
      var self = this;
      expiredCollection.listenTo(self, 'all', function() {
        this.reset(self.expired(), { 'vendorId' : self.vendorId });
      });
      return expiredCollection;
    }
  });
  return DealsCollection;
});
