import CustomerWrapper from "./wrappers/CustomerWrapper";
import Home from "../pages/customerPages/pages/public/home/Home";
import Login from "../pages/global/login/Login";
import UnauthorizedAccess from "../pages/global/components/UnauthorizedAccess";
import AccountActivation from "../pages/global/components/AccountActivation";
import RegisterPage from "../pages/global/components/RegisterPage";

const CustomerRoutes = [
    {   
        id:1,
        path: "/",
        name: "Incio",
        component: () => (
            <CustomerWrapper>
                <Home/>
            </CustomerWrapper>
        ),
        isPrivate: false,
    },
    {   
        id:2,
        path: "/login",
        name: "inciar sesion",
        component: () => (
            <CustomerWrapper>
                <Login/>
            </CustomerWrapper>
        ),
        isPrivate: false,
    },
    {   
        id:3,
        path: "/unauthorized-access",
        name: "Acceso no autorizado",
        component: () => (
            <CustomerWrapper>
                <UnauthorizedAccess/>
            </CustomerWrapper>
        ),
        isPrivate: false,
    },
    {
        id:4,
        path: "/account-activation",
        name: "Activacion de cuenta",
        component: () => (
            <CustomerWrapper>
                <AccountActivation/>
            </CustomerWrapper>
        ),
        isPrivate: false,
    },
    {
        id:5,
        path: "/register",
        name: "registro de cuenta",
        component: () => (
            <CustomerWrapper>
                <RegisterPage/>
            </CustomerWrapper>
        ),
        isPrivate: false,
    },


    
];

export default CustomerRoutes;