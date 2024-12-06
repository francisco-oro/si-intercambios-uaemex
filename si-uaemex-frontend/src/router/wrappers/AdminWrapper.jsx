import PropTypes from 'prop-types';
import { default as AdminHeader } from "../../pages/adminPages/pages/global/components/Header";
import { default as AdminFooter } from "../../pages/adminPages/pages/global/components/Footer";


const AdminWrapper = ({ children }) => {
    return (

        <>
            <AdminHeader />
            {children}
            <AdminFooter/>
        </>

    );
}

AdminWrapper.propTypes = {
    children: PropTypes.node
};

export default AdminWrapper;
