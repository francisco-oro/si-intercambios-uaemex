import { createSlice } from "@reduxjs/toolkit";
import axios from "axios";
import { setIsLoading } from "../../globalSlices/spinner.slicer";
import { message} from 'antd';
import getConfig, { Connection } from "../../../../utils/getConfig";

export const customerUsersModule = createSlice({
    name: 'customerUsersModule',
    initialState: {
        usersList: {},
        pageNumber:10,
    },
    reducers: {
        setUsersList: (state, action) => {
            state.usersList = action.payload
        },
        setPageNumber: (state, action) => {
            state.pageNumber = action.payload
        },
    }
});

export const getUsersListThunk = (sorted = 'asc') => async (dispatch) => {
    dispatch(setIsLoading(true));

    try {
        const res = await axios.get(Connection + `users?sortBy=firstName&sortOrder=${sorted}&pageSize=30`, getConfig()
        );
        dispatch(setUsersList(res.data.data));
    } catch (error) {
        console.error(error);
        // message.error('Ocurrió un error al obtener la lista de usuarios.'); 
    } finally {
        dispatch(setIsLoading(false));
    }
};

export const addUserThunk = (userData, userAddMsg) => dispatch => {
    dispatch(setIsLoading(true))
    axios.post(Connection + 'users', userData, getConfig())
        .then(res => {dispatch(getUsersListThunk())
            message.success(userAddMsg); 
        })
        .catch(error => {
            const errorMsg = error.response.data.msg 
            message.error(errorMsg); 
        })
        .finally(() => dispatch(setIsLoading(false)));
}

export const deleteUserThunk = (email, clinicDeletedMsg) => dispatch => {
    dispatch(setIsLoading(true))
    axios.delete(Connection + `users/${email}`, getConfig())
        .then(res => {dispatch(getUsersListThunk())
            message.success(clinicDeletedMsg);
        })
        .catch(error => {
            const errorMsg = error.response.data.msg 
            message.error(errorMsg); 
        })
        .finally(() => dispatch(setIsLoading(false)));
}


export const { setUsersList, setPageNumber } = customerUsersModule.actions;


export default customerUsersModule.reducer;




