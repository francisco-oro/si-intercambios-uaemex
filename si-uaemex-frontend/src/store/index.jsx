import { configureStore } from '@reduxjs/toolkit'
import  generalStates  from './slices/globalSlices/generalStates.slice'
import  customerUsersModule  from './slices/Admin/customers/custumers-usersModule.slice'
import  spinnerSlice  from './slices/globalSlices/spinner.slicer'
import authSlice from './slices/globalSlices/auth.slice'
import customerVendorsModule  from './slices/Admin/customers/customers-vendorsModule.slice'


export default configureStore({
  reducer: {
    //? globalStates 
    generalStates:generalStates,
    spinnerSlice:spinnerSlice,
    authentication: authSlice,

    // ? Rutas Administrador.
    customerUsersModule:customerUsersModule,
    customerVendorsModule: customerVendorsModule
  }
})
