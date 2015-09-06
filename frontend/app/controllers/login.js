import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    signUp: function() {
      $.post('/user', {
        first_name: this.get('firstName'),
        last_name: this.get('lastName'),
        email: this.get('sEmail'),
        password: this.get('sPassword')
      }).then(function() {
        document.location = "/dashboard";
      }, function() {
        this.set("loginFailed", true);
      }.bind(this));
    },

    authenticate: function() {
      var credentials = this.getProperties('email', 'password');
      var authenticator = 'simple-auth-authenticator:token';

      this.get('session').authenticate(authenticator, credentials);
    }
  }
});
