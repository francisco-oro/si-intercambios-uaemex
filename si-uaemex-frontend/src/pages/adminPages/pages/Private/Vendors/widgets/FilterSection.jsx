import { Radio, Row, Col } from 'antd';
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setPageNumber } from '../../../../../../store/slices/Admin/customers/customers-vendorsModule.slice';
import { useTranslation } from 'react-i18next';

const FilterSection = ({onClose, setSortedData}) => {
    const {t} = useTranslation('admin')
    const dispatch = useDispatch();

    const [selectedValues, setSelectedValues] = useState({
        showBy: 10,      
        orderBy: 'asc',  
    });

    const handleShowByChange = (e) => {
        setSelectedValues((prev) => ({ ...prev, showBy: e.target.value }));
        dispatch(setPageNumber(e.target.value),
        onClose()
    )
    };

    const handleOrderByChange = (e) => {
        console.log(e.target.value);
        setSelectedValues((prev) => ({ ...prev, orderBy: e.target.value }));
        setSortedData(e.target.value);
        onClose()
    };

    return (
        <div className="container mt-2 d-flex flex-column gap-2 bg-white mt-3 rounded-3 py-4">
            <div className="col-9 col-md-3 w-100 mt-3">
                <h6>{t("filterTitle1")}</h6>
                <Radio.Group
                    value={selectedValues.showBy}
                    onChange={handleShowByChange}
                    style={{ width: '100%' }}
                >
                    <Row className='d-flex flex-column gap-1'>
                        <Col span={24}>
                            <Radio value={5}>5</Radio>
                        </Col>
                        <Col span={24}>
                            <Radio value={10}>10</Radio>
                        </Col>
                        <Col span={24}>
                            <Radio value={15}>15</Radio>
                        </Col>
                        <Col span={24}>
                            <Radio value={20}>20</Radio>
                        </Col>
                    </Row>
                </Radio.Group>
            </div>

            <br />
            
            <div className="col-9 col-md-3 w-100">
                <h6>{t("filterName2")}</h6>
                <Radio.Group
                    value={selectedValues.orderBy}
                    onChange={handleOrderByChange}
                    style={{ width: '100%' }}
                >
                    <Row className='d-flex flex-column gap-1'>
                        <Col span={24}>
                            <Radio value={"desc"} >{t("desc")}</Radio>
                        </Col>
                        <Col span={24}>
                            <Radio value={"asc"}>{t("asc")}</Radio>
                        </Col>
                        {/* <Col span={24}>
                            <Radio value="active">{t("active")}</Radio>
                        </Col>
                        <Col span={24}>
                            <Radio value="inactive">{t("inactive")}</Radio>
                        </Col> */}
                    </Row>
                </Radio.Group>
            </div>
        </div>
    );
};

export default FilterSection;
