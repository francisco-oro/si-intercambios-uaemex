import PropTypes from 'prop-types';
import { default as DoctorHeader } from "../../pages/doctorPages/pages/global/components/Header";
import { default as DoctorFooter } from "../../pages/doctorPages/pages/global/components/Footer";


const DoctorWrapper = ({ children }) => {
    return (

        <>
             <DoctorHeader />
            {children}
            <DoctorFooter/>
        </>

    );
}

DoctorWrapper.propTypes = {
    children: PropTypes.node
};

export default DoctorWrapper;
