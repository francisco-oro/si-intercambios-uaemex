import AdminWrapper from "./wrappers/AdminWrapper";
import Home from "../pages/adminPages/pages/public/home/Home";
import Users from "../pages/adminPages/pages/Private/users/Users";

const AdminRoutes = [
    {   
        id:1,
        path: "/admin",
        name: "Home",
        component: () => (
            <AdminWrapper>
                <Home/>
            </AdminWrapper>
        ),
        isPrivate: true,
    },
    {   
        id:2,
        path: "/admin/users",
        name: "Usuarios",
        component: () => (
            <AdminWrapper>
                <Users/>
             </AdminWrapper>
        ),
        isPrivate: true,
    },


    
];

export default AdminRoutes;