import React, { useEffect, useMemo, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getUsersListThunk, deleteUserThunk } from '../../../../../../store/slices/Admin/customers/custumers-usersModule.slice';
import { Space, Table, Tag, Input, Button, Tooltip } from 'antd';
import { ClearOutlined, DeleteTwoTone, LoadingOutlined, ReloadOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';

const UsersTable = ({ sorted }) => {
  const { t } = useTranslation('admin')
  const dispatch = useDispatch();
  const data = useSelector((state) => state.customerUsersModule.usersList);
  const pageNum = useSelector(state => state.customerUsersModule.pageNumber)
  const usersTotal = data.length;
  const [searchText, setSearchText] = useState('');

  const formattedData = Array.isArray(data)
    ? data.map((user, index) => ({
      key: user.id,
      id: index + 1,
      nombre: `${user.firstName} ${user.lastName}`,
      firstName: user.firstName,
      lastName: user.lastName,
      email: user.email,
      active: user.active,
    }))
    : [];

  const filteredData = formattedData.filter(
    (user) =>
      user.firstName.toLowerCase().includes(searchText.toLowerCase()) ||
      user.lastName.toLowerCase().includes(searchText.toLowerCase()) ||
      user.email.toLowerCase().includes(searchText.toLowerCase())
  );

  useEffect(() => {
    dispatch(getUsersListThunk(sorted));
  }, [dispatch, usersTotal, sorted]);

  const handleDeleteUser = (email) => {
    const userDeletedMsg = t("userDeletedMsg")
    dispatch(deleteUserThunk(email, userDeletedMsg));
  };

  const columns = [
    {
      title: "Id", // Corregido el uso de i18n
      dataIndex: 'id',
      key: 'index',
    },
    {
      title: t("fullName"), // Corregido el uso de i18n
      dataIndex: 'nombre',
      key: 'nombre',
    },
    {
      title: t("email"), // Corregido el uso de i18n
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: t("status"), // Corregido el uso de i18n
      dataIndex: 'active',
      key: 'active',
      align: 'center',
      render: (active) => (
        <Tag color={active ? 'green' : 'volcano'}>
          {active ? t('active') : t('inactive')} {/* Traducción del estado */}
        </Tag>
      ),
    },
    {
      title: t("actions"), // Corregido el uso de i18n
      key: 'action',
      align: 'center',
      render: (_, record) => (
        <Space size="middle">
          <a onClick={() => handleDeleteUser(record.email)}>
            <Tooltip title={t('deleteUser')}>
              <DeleteTwoTone twoToneColor="#ff4d4f" />
            </Tooltip>
          </a>
          <a onClick={() => handleDeleteUser(record.email)}>
            <Tooltip title={t('updateUser')}>
              <ReloadOutlined style={{color:"#b25f06"}} />
            </Tooltip>
          </a>
        </Space>
      ),
    },
  ];


  const handleSearchChange = (e) => {
    setSearchText(e.target.value);
  };


  return (
    <div style={{ width: '100%' }}>
      <div className='position-relative'>
        <Input
          placeholder={t('searchBar')}
          value={searchText}
          onChange={handleSearchChange}
          style={{ marginBottom: 20, width: '100%' }}
        />
        <Tooltip title={t('clearField')}>
          <Button className='position-absolute' style={{ right: "10px", top: "0px", border: "none", background: "transparent" }} onClick={() => setSearchText('')}><ClearOutlined /></Button>
        </Tooltip>

      </div>
      <div style={{ width: '100%', overflowX: 'auto' }}>
        <Table
          columns={columns}
          dataSource={filteredData}
          size="small"
          pagination={{ pageSize: pageNum }}
          scroll={{ x: 'max-content' }}
        />
        <p className="position-absolute" style={{ marginTop: '-25px', fontSize: "13px" }}>
          <b>{t('totalUsers')}</b> {usersTotal}
        </p>
      </div>
    </div>
  );
};

export default UsersTable;
