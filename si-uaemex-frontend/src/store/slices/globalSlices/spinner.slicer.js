import { createSlice } from '@reduxjs/toolkit';

export const spinnerSlice = createSlice({
	name: 'spinner',
    initialState: false,
    reducers: {
        setIsLoading: (state, action) => {
            return action.payload
        }
    }
})


export const { setIsLoading } = spinnerSlice.actions;

export default spinnerSlice.reducer;