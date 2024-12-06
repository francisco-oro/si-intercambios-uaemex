import React from 'react';
import noDataIlustration from '../../../../public/NoDataFound.png';
import { Button } from 'antd';
import { useNavigate } from 'react-router-dom';

const NotFound404 = () => {
    const navigate = useNavigate();

    return (
        <div className='d-flex justify-content-center align-items-center vh-100'>
            <div className='row w-100'>
                <div className='col-6 d-flex justify-content-center'>
                    <img 
                        src={noDataIlustration} 
                        alt="Not Found" 
                        className='img-fluid'
                        style={{ objectFit: 'contain', maxHeight: '100%', maxWidth: '100%' }} 
                    />
                </div>

                <div className='col-6 d-flex flex-column justify-content-center align-items-center'>
                    <p className='text-center'>Lo sentimos, la ruta no existe.</p>
                    <Button className='orange-btn' onClick={() => navigate('/')}> Volver al incio </Button>
                </div>
            </div>
        </div>
    );
};

export default NotFound404;
