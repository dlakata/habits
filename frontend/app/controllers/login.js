import Ember from 'ember';

export default Ember.Controller.extend({
  loginFailed: false,
  signupFailed: false,
  isProcessing: false,

  actions: {
    signUp: function() {
      this.setProperties({
        signupFailed: false,
        isProcessing: true
      });

      $.post('http://localhost:5000/user', {
        first_name: this.get('firstName'),
        last_name: this.get('lastName'),
        email: this.get('sEmail'),
        password: this.get('sPassword')
      }).then(function() {
        this.set('isProcessing', false);
        document.location = '/dashboard';
      }.bind(this), function() {
        this.set('isProcessing', false);
        this.set("signupFailed", true);
      }.bind(this));
    },

    authenticate: function() {
      this.set('loginFailed', false);
      var credentials = {
        identification: this.get('email'),
        password: this.get('password')
      };
      var authenticator = 'simple-auth-authenticator:token';

      this.get('session').authenticate(authenticator, credentials);
      if ($.isEmptyObject(this.get('session').get('content').secure)) {
        this.set('loginFailed', true);
      }
    }
  }
});
