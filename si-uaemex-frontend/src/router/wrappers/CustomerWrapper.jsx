import PropTypes from 'prop-types';
import { default as CustomerHeader } from "../../pages/customerPages/pages/global/components/Header";
import { default as CustomerFooter } from "../../pages/customerPages/pages/global/components/Footer";
import MenuBar from "../../pages/customerPages/pages/global/components/MenuBar.jsx";


const CustomerWrapper = ({ children }) => {
    return (

        <>
            <MenuBar />
            {children}
            <CustomerFooter/>
        </>

    );
}

CustomerWrapper.propTypes = {
    children: PropTypes.node
};

export default CustomerWrapper;
