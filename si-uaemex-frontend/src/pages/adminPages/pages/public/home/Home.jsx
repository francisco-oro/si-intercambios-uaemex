import React, { useState } from 'react';
import { Breadcrumb, Layout, Menu } from 'antd';
import Users from '../../Private/users/Users';
import Doctors from '../../Private/Doctors/Doctors';
import Vendors from '../../Private/Vendors/Vendors';
import { useTranslation } from 'react-i18next';
import '../../../../../utils/translation/admin/usersModule';

const { Header, Content } = Layout;

const Home = () => {
  const { t } = useTranslation('admin');
  const [selectedTab, setSelectedTab] = useState('2');

  // Definir las tabs con las claves correctas
  const tabs = [
    { key: '1', label: t('tabDoctors') },
    { key: '2', label: t('tabUsers') },
    { key: '3', label: t('tabVendors') }
  ];

  // Manejar clic en las tabs
  const handleMenuClick = (e) => {
    setSelectedTab(e.key);
  };

  // Renderizar el contenido correspondiente basado en la tab seleccionada
  const renderContent = () => {
    switch (selectedTab) {
      case '1':
        return <Doctors />;
      case '2':
        return <Users />;
      case '3':
        return <Vendors />;
      default:
        return <Users />;
    }
  };

  return (
    <Layout>
      <Header
        style={{
          position: 'sticky',
          top: 0,
          zIndex: 1,
          width: '100%',
          display: 'flex',
          alignItems: 'center',
          padding: '0',
        }}
      >
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[selectedTab]} // Usar el estado para el menú
          onClick={handleMenuClick}
          style={{
            flex: 1,
            minWidth: 0,
          }}
          className="adminWrappersBg"
          items={tabs.map((tab) => ({
            key: tab.key,
            label: tab.label,
          }))}
        />
      </Header>
      <Content>
        <Breadcrumb
          style={{ padding: '16px 0' }}
          items={[
            { title: 'Home' },
            { title: tabs.find((tab) => tab.key === selectedTab)?.label },
          ]}
        />
        <div
          style={{
            paddingBottom: '20px',
          }}
        >
          {renderContent()}
        </div>
      </Content>
    </Layout>
  );
};

export default Home;
