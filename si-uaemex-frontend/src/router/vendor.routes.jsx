import VendorWrapper from "./wrappers/VendorWrapper";
import Home from '../pages/vendorPages/pages/public/home/Home'  ;

const VendorRoutes = [
    {   
        id:0,
        path: "/vendor",
        name: "Home",
        component: () => (
            <VendorWrapper>
                <Home/>
            </VendorWrapper>
        ),
        isPrivate: true,
    },


    
];

export default VendorRoutes;