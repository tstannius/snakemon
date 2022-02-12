import { apiUrl } from '../env';



const APIauthProvider = {
  isAuthenticated: false,

  async TestToken() {
    const request = new Request(`${apiUrl}/auth/test-token`, {
      method: 'POST',
      credentials: 'include', // necessary for cookies
    });

    const response = await fetch(request).then((response) => {
      if (response.ok) {
        return response.json();
      } else if (response.status === 500) {
        throw new Error('Internal server error');
      } else if (response.status > 400 && response.status < 500) {
        APIauthProvider.isAuthenticated = false;
        return null
      }
    })
    .then((data) => {
      var username = null;
      if ((data != null) && ('username' in data)) {
          username = data.username;
      }
      APIauthProvider.isAuthenticated = true;
      return username;
    })
    .catch((error) => {
      throw new Error(error);
    });
    return response;
  },


  async Signin(username: string, password: string) {
      // Assert username or password is not empty
      if (!(username.length > 0) || !(password.length > 0)) {
        throw new Error('Username or password was not provided');
      }
  
      // OAuth2 expects form data, not JSON data
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
    
      const request = new Request(`${apiUrl}/auth/access-token`, {
        method: 'POST',
        body: formData,
        credentials: 'include', // necessary for cookies
      });
    
      const response = await fetch(request).then((response) => {
        // return response if succesful / unsuccesful login
        if (response.status === 200 || 
          ((response.status >= 400) && (response.status <= 500))) {
          return response;
        } else if (response.status === 500) {
          throw new Error('Internal server error');
        } else {
          throw new Error('Something went wrong');
        }
      })
      .catch((error) => {
        throw new Error(error);
      });
      APIauthProvider.isAuthenticated = true;
      return response;
    },


    async Signout() {
      const request = new Request(`${apiUrl}/auth/delete-token`, {
        method: 'POST',
        credentials: 'include', // necessary for cookies
      });

      const response = await fetch(request).then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Something went wrong');
        }
      })
      .catch((error) => {
        throw new Error(error);
      });

      APIauthProvider.isAuthenticated = false;
      return response;
    },

    
    async signout(callback: VoidFunction) {
      APIauthProvider.Signout();
      callback();
    }
};


export { APIauthProvider };
