import React, { useState } from 'react';
import i18n from '../../../utils/i18n'; //! <--- No se va usar pero si la borras se pierde la traduccion.
import { useForm } from 'react-hook-form';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Button, Image } from 'antd';
import { useTranslation } from 'react-i18next';
import { accountActivationCodeThunk } from '../../../store/slices/globalSlices/auth.slice';

const AccountActivation = () => {

  const navigate = useNavigate();
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const { register, handleSubmit, formState: { errors }, reset } = useForm();

  const [focusedInput, setFocusedInput] = useState(null);
  const [isVisible, setIsVisible] = useState(false);

  const onSubmit = ({ email, activationCode }) => {
    const successMsg = t('activationSuccessfull');
    const userCredentials = {
      email: email,
      activationCode: Number(activationCode)
  }
  console.log(userCredentials)
    dispatch(accountActivationCodeThunk(userCredentials, successMsg));
    navigate('/admin');
    reset();
  };

  const clearFields = () => {
    reset();
  };

  return (
    <div className='container d-flex justify-content-center my-5' style={{height:"100vh"}}>
        <div>
      <div align="center">
        <Image src='./logo.png' preview={false} />
      </div>
      <form onSubmit={handleSubmit(onSubmit)} className='form-container'>
        {/* Campo de Correo Electrónico */}
        <div className='form-group'>
          <input
            type="email"
            placeholder={t('emailPlaceholder')}
            {...register('email', { required: t('emailRequired') })}
            className={`input ${focusedInput === 'email' ? 'input-focus' : ''}`}
            onFocus={() => setFocusedInput('email')}
            onBlur={() => setFocusedInput(null)}
          />
          {errors.email && <p className='error'>{errors.email.message}</p>}
        </div>

        {/* Campo de Contraseña */}
        <div className='form-group position-relative'>
          <input
            type='number'
            placeholder={t('activationCode')}
            {...register('activationCode', { required: t('passwordRequired') })}
            className={`input ${focusedInput === 'activationCode' ? 'input-focus' : ''}`}
            onFocus={() => setFocusedInput('activationCode')}
            onBlur={() => setFocusedInput(null)}
          />
          <i
            onClick={() => setIsVisible(!isVisible)}
            className={isVisible ? "bi bi-eye-slash" : "bi bi-eye"}
            style={{ position: "absolute", right: "10px", bottom: "5px", cursor: "pointer" }}
          ></i>
          {errors.activationCode && <p className='error'>{errors.activationCode.message}</p>}
        </div>

        {/* Botones */}
        <div className='w-100 d-flex gap-3 justify-content-end'>
          <Button htmlType="submit" className='mt-4 blue-btn'>{t("send")}</Button>
          <Button type="button" className='mt-4 orange-btn' onClick={clearFields}>{t("clearFieldsLogin")}</Button>
        </div>
      </form>
    </div>
 </div>
  );
};

export default AccountActivation;
