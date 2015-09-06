import DS from 'ember-data';

export default DS.Model.extend({
  title: DS.attr('string'),
  description: DS.attr('string'),
  frequency: DS.attr('number'),
  state_date: DS.attr('string'),
  user: DS.belongsTo('user')
});
