<Button
                className='col-3'
                type="default"
                style={{
                    backgroundColor: '#c2f2cd',  // Verde claro
                    borderColor: '#19a41b',      // Verde oscuro
                    color: '#19a41b',            // Texto verde oscuro
                    fontWeight: 'bold',
                    padding: '6px 20px'
                }}
            >
                <FilterOutlined /> Filtros
            </Button>








import { FilterOutlined } from '@ant-design/icons';
import { Button, Select } from 'antd';
import React, { useState } from 'react';

const FilterSection = () => {
    const [selectedValue, setSelectedValue] = useState(10);

    const handleChange = (value) => {
        setSelectedValue(value);
    };

    return (
        <div className=' container mt-2 d-flex'>
            <div className='col-9 col-md-3'>
                {/* Usamos el Select de Ant Design */}
                <Select
                    id="itemsPerPage"
                    value={selectedValue}
                    onChange={handleChange}
                    style={{ width: 200 }}  // Añadimos un estilo similar al ejemplo
                    placeholder="Mostrar por"
                >
                    <Select.Option value={5}>Mostrar por: 5</Select.Option>
                    <Select.Option value={10}>Mostrar por: 10</Select.Option>
                    <Select.Option value={15}>Mostrar por: 15</Select.Option>
                    <Select.Option value={20}>Mostrar por: 20</Select.Option>
                </Select>
            </div>
            <div className='col-9 col-md-3'>
                {/* Usamos el Select de Ant Design */}
                <Select
                id="itemsPerPage"
                value={selectedValue}
                onChange={handleChange}
                style={{ width: '100%' }} // Establecer el ancho al 100% del contenedor
                placeholder="Mostrar por"
            >
                <Select.Option value={5}>Alfabetico descendente</Select.Option>
                <Select.Option value={10}>Alfabetico ascendente</Select.Option>
                <Select.Option value={15}>Activos</Select.Option>
                <Select.Option value={20}>Inactivos</Select.Option>
            </Select>
            </div>
            
        </div>
    );
};

export default FilterSection;
