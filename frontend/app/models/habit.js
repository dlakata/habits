import DS from 'ember-data';

export default DS.Model.extend({
  title: DS.attr('string'),
  description: DS.attr('string'),
  frequency: DS.attr('number'),
  frequency_type: DS.attr('number'),
  user: DS.belongsTo('user')
});
