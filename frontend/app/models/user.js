import DS from 'ember-data';

export default DS.Model.extend({
  id: DS.attr('number'),
  first_name: DS.attr('string'),
  last_name: DS.attr('string'),
  email: DS.attr('string'),
  password: DS.attr('string'),
  habits: DS.hasMany('habit')
});
