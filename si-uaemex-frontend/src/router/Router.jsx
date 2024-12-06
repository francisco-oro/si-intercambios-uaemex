import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import CustomerRoutes from "./customer.routes";
import AdminRoutes from './admin.routes'
import DoctorRoutes from "./doctor.routes";
import VendorRoutes from "./vendor.routes";
import Loader from "../pages/global/components/Loader";
import { useSelector } from "react-redux";
import NotFound404 from "../pages/global/components/NotFound404";
import { useEffect } from "react";


const Router = () => {
  const isLoading = useSelector(state => state.spinnerSlice);
  const isAuthenticated = useSelector(state => state.authentication.isAuthenticated)


  return (
    <BrowserRouter>
      {isLoading && <Loader />}
      <Routes>

        {CustomerRoutes.map(({ component: Component, path, name, isPrivate }) => (
          <Route
            path={path}
            key={path}
            name={name}
            element={
              isPrivate && !isAuthenticated ? (
                <Navigate to="/unauthorized-access" />
              ) : (
                <Component
                />
              )
            }
          />
        ))}

        {AdminRoutes.map(({ component: Component, path, name, isPrivate }) => (
          <Route
            path={path}
            key={path}
            name={name}
            element={
              isPrivate && !isAuthenticated ? (
                <Navigate to="/unauthorized-access" />
              ) : (
                <Component
                />
              )
            }
          />
        ))}

        {DoctorRoutes.map(({ component: Component, path, name, isPrivate }) => (
          <Route
            path={path}
            key={path}
            name={name}
            element={
              isPrivate && !isAuthenticated ? (
                <Navigate to="/unauthorized-access" />
              ) : (
                <Component
                />
              )
            }
          />
        ))}

        {VendorRoutes.map(({ component: Component, path, name, isPrivate }) => (
          <Route
            path={path}
            key={path}
            name={name}
            element={
              isPrivate && !isAuthenticated ? (
                <Navigate to="/unauthorized-access" />
              ) : (
                <Component
                />
              )
            }
          />
        ))}
        <Route path="*" element={<NotFound404 />} />

      </Routes>
    </BrowserRouter>
  );
};

export default Router;