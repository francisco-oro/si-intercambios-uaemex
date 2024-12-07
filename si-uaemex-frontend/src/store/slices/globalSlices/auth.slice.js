import { createSlice } from "@reduxjs/toolkit";
import axios from 'axios';
import { Connection } from '../../../utils/getConfig';
import { message } from "antd";

export const authSlice = createSlice({
    name: 'authentication',
    initialState: {
        isAuthenticated: localStorage.getItem('token') ? true : false,
        token: localStorage.getItem('token') || null,
        isUserAllowed: false,
        loginError:{},
        decodedData: {},
    },
    reducers: {
        setUserToken: (state, action) => {
            state.isAuthenticated = true;
            state.token = action.payload.token;
            localStorage.setItem('token', action.payload.token);
        },
        clearUserToken: state => {
            state.isAuthenticated = false;
            state.token = null;
            localStorage.removeItem('token');
            state.currentUserId = null;
        
            //todo Eliminar caché
            if ('caches' in window) {
                caches.keys().then(cacheNames => {
                    cacheNames.forEach(cacheName => {
                        caches.delete(cacheName);
                    });
                });
            }
        },
        updateAuthState: (state, action) => {
            if (state.token !== action.payload.token) {
                state.isAuthenticated = true;
                state.token = action.payload.token;
                localStorage.setItem('token', action.payload.token);
            }
        },
        setIsUserAllowed:(state,action) => {
            state.isUserAllowed = action.payload
        },
        setErrorLogin:(state,action) => {
            state.loginError = action.payload
        },
        setDecodedData: (state, action) => {
            state.decodedData = action.payload
        }
    }
});

export const { setUserToken, clearUserToken, updateAuthState,setIsUserAllowed, setErrorLogin, setDecodedData } = authSlice.actions;

export const authenticationThunk = (userCredentials, successMsg) => dispatch => {
    axios.post(Connection + 'token/', userCredentials)
     .then(res => {
         const newToken = res.data.access;
         dispatch(updateAuthState({ token: newToken }));
         message.success(successMsg); 
     })
     .catch(error => {
        console.error('Error en la autenticación:', error);
        const errorMsg = error.response.data.msg 
        message.error(errorMsg)
     });
};

export const accountActivationCodeThunk = (userCredentials, successMsg) => dispatch => {
    axios.post(Connection + 'users/activate', userCredentials)
     .then(res => {
         message.success(successMsg); 
     })
     .catch(error => {
        console.error('Error en la autenticación:', error);
        const errorMsg = error.response.data.msg 
        message.error(errorMsg)
     });
};

export default authSlice.reducer;
