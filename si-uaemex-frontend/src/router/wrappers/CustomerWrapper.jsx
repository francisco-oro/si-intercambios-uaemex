import PropTypes from 'prop-types';
import { default as CustomerHeader } from "../../pages/customerPages/pages/global/components/Header";
import { default as CustomerFooter } from "../../pages/customerPages/pages/global/components/Footer";


const CustomerWrapper = ({ children }) => {
    return (

        <>
            <CustomerHeader />
            {children}
            <CustomerFooter/>
        </>

    );
}

CustomerWrapper.propTypes = {
    children: PropTypes.node
};

export default CustomerWrapper;
