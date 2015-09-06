import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    "add-habit": function() {
      var habit = this.store.createRecord('habit', this.getProperties('title', 'description'));
      habit.save().then(this.transitionToRoute('dashboard'));
    }
  }
});
