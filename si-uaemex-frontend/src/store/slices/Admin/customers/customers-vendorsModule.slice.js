import { createSlice } from "@reduxjs/toolkit";
import axios from "axios";
import { setIsLoading } from "../../globalSlices/spinner.slicer";
import { message} from 'antd';
import getConfig, { Connection } from "../../../../utils/getConfig";

export const customerVendorsModule = createSlice({
    name: 'customerVendorsModule',
    initialState: {
        vendorsList: {},
        pageNumber:10,
    },
    reducers: {
        setVendorsList: (state, action) => {
            state.vendorsList = action.payload
        },
        setPageNumber: (state, action) => {
            state.pageNumber = action.payload
        },
    }
});

export const getVendorsListThunk = () => async (dispatch) => {
    dispatch(setIsLoading(true));

    try {
        const res = await axios.get(Connection + `vendors`) ;
        dispatch(setVendorsList(res.data.data));
    } catch (error) {
        console.error(error);
        // message.error('Ocurrió un error al obtener la lista de usuarios.'); 
    } finally {
        dispatch(setIsLoading(false));
    }
};

export const addClinicThunk = (clinicData, clinicAddMsg) => dispatch => {
    dispatch(setIsLoading(true))
    axios.post(Connection + 'vendors', clinicData)
        .then(res => {dispatch(getVendorsListThunk())
            message.success(clinicAddMsg); 
        })
        .catch(error => {
            const errorMsg = error.response.data.msg 
            message.error(errorMsg); 
        })
        .finally(() => dispatch(setIsLoading(false)));
}

export const deleteClinicThunk = (key, userDeletedMsg) => dispatch => {
    dispatch(setIsLoading(true))
    axios.delete(Connection + `vendors/${key}`)
        .then(res => {dispatch(getVendorsListThunk())
            message.success(userDeletedMsg);
        })
        .catch(error => {
            const errorMsg = error.response.data.msg 
            message.error(errorMsg); 
        })
        .finally(() => dispatch(setIsLoading(false)));
}


export const { setVendorsList, setPageNumber } = customerVendorsModule.actions;


export default customerVendorsModule.reducer;




