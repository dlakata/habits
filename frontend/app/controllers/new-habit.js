import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    "add-habit": function() {
      this.store.createRecord('habit', this.getProperties('title', 'description'));
      this.transitionToRoute('dashboard');
    }
  }
});
