import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    return [{
      title: "Go to the gym",
      description: "Make sure to work out at the gym for at least 30 minutes a day"
    }, {
      title: "Brush teeth",
      description: "Brush teeth twice a day or after every meal"
    }];
  }
});
