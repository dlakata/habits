import DS from 'ember-data';

export default DS.Model.extend({
  id: DS.attr('number'),
  time: DS.attr('number'),
  goal: DS.attr('number'),
  title: DS.attr('string'),
  description: DS.attr('string')
});
