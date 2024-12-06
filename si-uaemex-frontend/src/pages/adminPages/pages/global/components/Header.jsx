import React from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setUserRol } from '../../../../../store/slices/globalSlices/generalStates.slice';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { useTranslation } from 'react-i18next';
import { clearUserToken } from '../../../../../store/slices/globalSlices/auth.slice';
import { Image } from 'antd';

const Header = () => {
  const { t, i18n } = useTranslation();

  const switchLanguage = (lang) => {
    i18n.changeLanguage(lang);
  };

  const navigate = useNavigate()
  const dispatch = useDispatch()

  const log = () => {
    dispatch(setUserRol(''))
    navigate('/login')

  }

  const logout = () => {
    dispatch(clearUserToken());
    navigate('/')
  }

  return (

    <Navbar className="">
      <Container className='d-flex justify-content- align-items-center'>

      <div className='w-50 text-start'>
          {/*<Navbar.Brand onClick={() => navigate('/')} className=''>Pet-Vet :{')'}</Navbar.Brand>*/}
          <Navbar.Brand onClick={() => navigate('/')} className=''>
            <Image
              width={250}
              src="./logo.png"
              preview={false}
            /></Navbar.Brand>
        </div>

        <div className='d-flex gap-5'>

          <NavDropdown title={t('languageLabel')} id="basic-nav-dropdown" className='d-flex align-items-center'>
            <NavDropdown.Item onClick={() => switchLanguage('en')}> {t('languageEnglish')}</NavDropdown.Item>

            <NavDropdown.Item onClick={() => switchLanguage('es')}>{t('languageSpanish')}</NavDropdown.Item>
          </NavDropdown>

          {/* icono de menu hamburguesa */}
          <Navbar.Toggle aria-controls="basic-navbar-nav" />

          <Nav>
            <NavDropdown title={t('menuLabel')} id="basic-nav-dropdown">
              <NavDropdown.Item onClick={log}>{t('loginLabel')}</NavDropdown.Item>

              <NavDropdown.Item onClick={() => navigate('/')}>{t('homeLabel')}</NavDropdown.Item>

              <NavDropdown.Item onClick={() => navigate('/admin/users')}>{t('usersLabel')}</NavDropdown.Item>

              <NavDropdown.Divider />

              <NavDropdown.Item onClick={logout}>
                {t('logoutLabel')}
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </div>

      </Container>
    </Navbar>
  );
};

export default Header;
