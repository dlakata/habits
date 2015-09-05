export default Ember.Handlebars.makeBoundHelper(function(habit) {
  return 100 * habit.time / habit.goal;
});
