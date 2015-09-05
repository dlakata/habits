import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    habitDone: function(_status, habit) {
      console.log("You clicked " + _status + " for " + habit.title + "!");
    }
  }
});
