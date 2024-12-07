import React, { useState } from 'react';
import i18n from '../../../../utils/i18n'; //! <--- No se va usar pero si la borras se pierde la traduccion.
import { useForm } from 'react-hook-form';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Button, Image } from 'antd';
import { useTranslation } from 'react-i18next';
import { authenticationThunk } from '../../../../store/slices/globalSlices/auth.slice'
const LoginForm = () => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { errors }, reset } = useForm();

  const [focusedInput, setFocusedInput] = useState(null);
  const [isVisible, setIsVisible] = useState(false);

  const onSubmit = ({ username, password }) => {
    const successMsg = t('logInSuccess');
    const userCredentials = { username, password };
    dispatch(authenticationThunk(userCredentials, successMsg));
    navigate('/');
    reset();
  };

  const clearFields = () => {
    reset();
  };

  return (
    <div>
      <div align="center">
        <Image src='./logo.png' preview={false} />
      </div>
      <form onSubmit={handleSubmit(onSubmit)} className='form-container'>
        {/* Campo de Correo Electrónico */}
        <div className='form-group'>
          <input
            type="text"
            placeholder={t('Número de cuenta')}
            {...register('username', { required: t('emailRequired') })}
            className={`input ${focusedInput === 'username' ? 'input-focus' : ''}`}
            onFocus={() => setFocusedInput('username')}
            onBlur={() => setFocusedInput(null)}
          />
          {errors.username && <p className='error'>{errors.username.message}</p>}
        </div>

        {/* Campo de Contraseña */}
        <div className='form-group position-relative'>
          <input
            type={isVisible ? "text" : "password"}
            placeholder={t('passwordPlaceholder')}
            {...register('password', { required: t('passwordRequired') })}
            className={`input ${focusedInput === 'password' ? 'input-focus' : ''}`}
            onFocus={() => setFocusedInput('password')}
            onBlur={() => setFocusedInput(null)}
          />
          <i
            onClick={() => setIsVisible(!isVisible)}
            className={isVisible ? "bi bi-eye-slash" : "bi bi-eye"}
            style={{ position: "absolute", right: "10px", bottom: "5px", cursor: "pointer" }}
          ></i>
          {errors.password && <p className='error'>{errors.password.message}</p>}
        </div>

        {/* Botones */}
        <div className='w-100 d-flex gap-3 justify-content-end'>
          <Button htmlType="submit" className='mt-4 blue-btn'>{t("sendDataLogin")}</Button>
          <Button type="button" className='mt-4 orange-btn' onClick={clearFields}>{t("clearFieldsLogin")}</Button>
        </div>
      </form>
    </div>
  );
};

export default LoginForm;
