import React, { useState } from 'react';
import { Drawer, Button } from 'antd';
import { CloseOutlined } from '@ant-design/icons';

const GeneralDrawer = ({
    title,
    headerContent,
    bodyContent,
    footerContent,
    visible,
    onClose
}) => {
    return (
        <Drawer
            title={null}  
            placement="left"  
            width="70%"         
            open={visible}  
            onClose={onClose}  
            closable={false}  
            className='d-flex flex-column'
        >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h5>
                    {title || 'Drawer Title'}</h5> 
                <Button
                    onClick={onClose}
                    type="link"
                    className='closingX'

                >
                    <CloseOutlined />
                </Button>
            </div>

            {/* Cuerpo del Drawer */}
            <div>
                {bodyContent}
            </div>

            {/* Footer personalizado */}
            {footerContent && (
                <div>
                    {footerContent}
                </div>
            )}
        </Drawer>
    );
};

export default GeneralDrawer;
