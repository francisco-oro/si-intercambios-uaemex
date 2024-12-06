import React from 'react';
import unauthorized from '../../../../public/unauthorized.jpg';
import { Button } from 'antd';

const UnauthorizedAccess = () => {
    return (
        <div className='d-flex justify-content-center align-items-center vh-100'>
            <div className='row w-100'>
                <div className='col-6 d-flex justify-content-center'>
                    <img 
                        src={unauthorized} 
                        alt="Not Found" 
                        className='img-fluid'
                        style={{ objectFit: 'contain', maxHeight: '100%', maxWidth: '100%' }} 
                    />
                </div>
                <div className='col-6 d-flex flex-column justify-content-center align-items-center'>
                    <p className='text-center'>No tienes acceso a este contenido.</p>
                    <Button className='orange-btn'> Volver al incio </Button>
                </div>
            </div>
        </div>
    );
};

export default UnauthorizedAccess;
