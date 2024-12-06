import { createSlice } from "@reduxjs/toolkit";

export const generalStates = createSlice({
    name: 'generalStates',
    initialState: {
        isDesktopSize: false,
        userRol: ""
    },
    reducers: {
        setIsDesktopSize:(state,action) => {
            state.isDesktopSize = action.payload
        },
        setUserRol:(state,action) => {
            state.userRol = action.payload
        }

    }
});

export const { setIsDesktopSize,setUserRol} = generalStates.actions;


export default generalStates.reducer;
