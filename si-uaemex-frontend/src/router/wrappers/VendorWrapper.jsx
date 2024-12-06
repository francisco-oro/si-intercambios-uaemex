import PropTypes from 'prop-types';
import { default as VendorHeader } from "../../pages/vendorPages/pages/global/components/Header";
import { default as VendorFooter } from "../../pages/vendorPages/pages/global/components/Footer";


const VendorWrapper = ({ children }) => {
    return (

        <>
            <VendorHeader />
            {children}
            <VendorFooter/>
        </>

    );
}

VendorWrapper.propTypes = {
    children: PropTypes.node
};

export default VendorWrapper;
