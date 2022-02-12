import React, { createContext, useContext, useEffect, useState } from 'react';
import { APIauthProvider } from "../utils/auth";

interface AuthContextType {
    user: any;
    signin: (user: string, password: string, callbackSucces: VoidFunction, callbackError: Function) => void;
    signout: (callback: VoidFunction) => void;
  }
  
export let AuthContext = createContext<AuthContextType>(null!);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    let [user, setUser] = useState<any>(null);

    useEffect(() => {
        APIauthProvider.TestToken().then((result) => {
            setUser(result);
        });
      }, [])

    let signin = (username: string, 
                    password: string, 
                    callbackSucces: VoidFunction, 
                    callbackError: Function) => {
        // callback func is to call setUser of the AuthProvider AND the callback
        // to the AuthProvider signin func
        return APIauthProvider.Signin(username, password)
                .then((response) => {
                    if (response.status === 200) {
                        setUser(username);
                        callbackSucces();
                    } else if ((response.status >= 400) && (response.status <= 500)) {
                        response.json()
                            .then(data => {
                                callbackError(data.detail)
                            })
                    }
                });
    };

    let signout = (callback: VoidFunction) => {
        return APIauthProvider.signout(() => {
        setUser(null);
        callback();
        });
    };

    let value = { user, signin, signout };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
    return useContext(AuthContext);
}
