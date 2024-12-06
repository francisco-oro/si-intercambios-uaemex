import React from 'react';
import { Button, Modal } from 'antd';
import { CloseOutlined } from '@ant-design/icons';

const GeneralModal = ({
  title = 'Modal Title',    // Título predeterminado
  bodyContent,             // Contenido del cuerpo (se pasa como prop)
  footerContent,           // Contenido del pie (se pasa como prop)
  visible,                 // Controla la visibilidad del modal
  onClose,                 // Función para cerrar el modal
}) => {
  return (
    <Modal
      title={null}          // Título del Modal
      open={visible}      // Controla si el modal es visible
      onCancel={onClose}     // Función que se llama cuando el modal se cierra
      footer={null} // Pie de modal personalizado (si se pasa)
      centered               // Centra el modal en la pantalla
      width={500}            // Ancho del modal (ajústalo según tus necesidades)
      destroyOnClose         // Destruye el modal cuando se cierra, lo que elimina cualquier estado residual
      closable={false}       // Desactivamos el botón de cierre por defecto
    >

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h5>
          {title || 'Modal Title'}</h5>  {/* Título del Drawer */}
        <Button
          onClick={onClose}
          type="link"
          className='closingX'
>
          <CloseOutlined />
        </Button>
      </div>
      <div>{bodyContent}</div>
    </Modal>
  );
};

export default GeneralModal;
