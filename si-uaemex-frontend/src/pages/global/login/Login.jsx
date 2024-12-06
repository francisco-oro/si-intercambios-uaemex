import React from 'react';
import LoginForm from './widgets/LoginForm'
import i18n from '../../../utils/i18n'; //! <--- No se va usar pero si la borras se pierde la traduccion.
import { useTranslation } from 'react-i18next';

const Login = () => {
    const { t } = useTranslation('common');

    return (
        <div className='container d-flex justify-content-center my-5' style={{height:"100vh"}}>

            <div  >
                <LoginForm />
            </div>
        </div>
    );
};

export default Login;