import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { Button } from 'antd';
import { FilterOutlined, UserAddOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';
import FilterSection from './widgets/FilterSection'
import GeneralDrawer from '../../../../global/components/GeneralDrawer';
import GeneralModal from '../../../../global/components/GeneralModal';
import UsersForm from './components/UsersForm';
import '../../../../../utils/translation/admin/usersModule'
import UsersTable from './components/UsersTable';

const Doctors = () => {
  const {t} = useTranslation('admin')
  const isDesktop = useSelector(state => state.generalStates.isDesktopSize);
  const [visibleDrawer, setVisibleDrawer] = useState(false);

  const showDrawer = () => setVisibleDrawer(true);
  const closeDrawer = () => setVisibleDrawer(false);

  const [visibleModal, setVisibleModal] = useState(false);
  const showModal = () => setVisibleModal(true);
  const closeModal = () => setVisibleModal(false);

  const [sortedData, setSortedData] = useState('asc')

  useEffect(() => {

  },[isDesktop])

  return (
    <div className="container mt-5">
      <div className="row">
        {isDesktop ? (
          <div className="col-12 col-md-3">

            <Button
              className="col-7 mb-2 blue-btn"
              type="default"
              onClick={showModal}
              style={{
                padding: '6px 20px',
              }}
            >
              <UserAddOutlined />{t('addVendor')}
            </Button>
            <FilterSection onClose={closeDrawer} setSortedData={setSortedData}/>
          </div>
        ) : (
          <>
        <div className='col-12'>
            <div className='col-12'>
              <Button
                type="default"
                className='mb-2 green-btn'
                onClick={showDrawer}
              >
                <FilterOutlined /> {t('filterButton')}
              </Button>
            </div>
              <Button
                className='mb-2 blue-btn'
                type="default"
                onClick={showModal}
                style={{
                  padding: '6px 20px',
                }}
              >
                <UserAddOutlined /> {t('addUser')}
              </Button>
            </div>
            <GeneralDrawer
              title={<div className='d-flex gap-4'><FilterOutlined style={{ color: "#19a41b" }} /><h6 className='mt-1'>{t('filterTitle')}</h6></div>}
              visible={visibleDrawer}
              onClose={closeDrawer}
              bodyContent={<FilterSection onClose={closeDrawer} setSortedData={setSortedData}/>}
            />
          </>
        )}

        <div className="col-12 col-md-9">
          <UsersTable sorted={sortedData}/>
        </div>
      </div>

      <GeneralModal
        title={<div className='d-flex gap-4'><UserAddOutlined style={{ color: "#1971a4" }} /><h5 className='mt-1'>{t('AddUserTitle')}</h5></div>}
        visible={visibleModal}
        onClose={closeModal}
        bodyContent={<UsersForm onClose={closeModal} />}
      />
    </div>
  );
};

export default Doctors;
