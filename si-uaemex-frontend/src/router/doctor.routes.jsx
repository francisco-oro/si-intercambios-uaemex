import DoctorWrapper from "./wrappers/DoctorWrapper";
import Home from "../pages/doctorPages/pages/public/home/Home";

const DoctorRoutes = [
    {   
        id:0,
        path: "/doctor",
        name: "Home",
        component: () => (
            <DoctorWrapper>
                <Home/>
            </DoctorWrapper>
        ),
        isPrivate: true,
    },


    
];

export default DoctorRoutes;