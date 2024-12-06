import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useDispatch, useSelector } from 'react-redux';
import { Button, Image } from 'antd';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

const RegisterPage = ({ onClose }) => {
    const { t } = useTranslation('admin')
    const navigate = useNavigate();
    const isDesktop = useSelector(state => state.generalStates.isDesktopSize);
    const { register, handleSubmit, formState: { errors }, reset } = useForm();
    const dispatch = useDispatch();

    const [focusedInput, setFocusedInput] = useState(null);

    const onSubmit = ({ firstName, lastName, email, password, dob }) => {
        const userAddMsg = t("newUserMsg")
        const userData = {
            firstName,
            lastName,
            email,
            password,
            dob
        };
        reset();
        // dispatch(addUserThunk(userData, userAddMsg));
        navigate('/activation-account');
        onClose();
    };
    const clear = () => {
        reset()
    }

    return (
        <div className='container d-flex justify-content-center my-5' style={{ height: "100vh" }}>
            <div>
                <div align="center">
                    <Image src='./logo.png' preview={false} />
                </div>
                <form onSubmit={handleSubmit(onSubmit)} className='form-container'>
                    {/* Nombre */}
                    <div className={isDesktop ? 'd-flex w-100 gap-3' : 'w-100'}>
                        <div className='form-group'>
                            <input
                                type="text"
                                placeholder={t("firstName")}
                                {...register('firstName', { required: t("firstNameErr") })}
                                className={`input ${focusedInput === 'firstName' ? 'input-focus' : ''}`}
                                onFocus={() => setFocusedInput('firstName')}
                                onBlur={() => setFocusedInput(null)}
                            />
                            {errors.firstName && <p className='error'>{errors.firstName.message}</p>}
                        </div>

                        {/* Apellido */}
                        <div className='form-group'>
                            <input
                                type="text"
                                placeholder={t("lastName")}
                                {...register('lastName', { required: t("lastNameErr") })}
                                className={`input ${focusedInput === 'lastName' ? 'input-focus' : ''}`}
                                onFocus={() => setFocusedInput('lastName')}
                                onBlur={() => setFocusedInput(null)}
                            />
                            {errors.lastName && <p className='error'>{errors.lastName.message}</p>}
                        </div>
                    </div>

                    {/* Correo electrónico y Contraseña */}
                    <div className='form-group'>
                        <input
                            type="email"
                            placeholder={t("email")}
                            {...register('email', { required: t("emailErr") })}
                            className={`input ${focusedInput === 'email' ? 'input-focus' : ''}`}
                            onFocus={() => setFocusedInput('email')}
                            onBlur={() => setFocusedInput(null)}
                        />
                        {errors.email && <p className='error'>{errors.email.message}</p>}
                    </div>

                    <div className='form-group'>
                        <input
                            type="password"
                            placeholder={t("password")}
                            {...register('password', { required: t("passwordErr") })}
                            className={`input ${focusedInput === 'password' ? 'input-focus' : ''}`}
                            onFocus={() => setFocusedInput('password')}
                            onBlur={() => setFocusedInput(null)}
                        />
                        {errors.password && <p className='error'>{errors.password.message}</p>}
                    </div>

                    {/* Fecha de nacimiento */}

                    <div className={isDesktop ? 'd-flex w-100 gap-3' : 'w-100'}>
                        <div className='form-group'>
                            <input
                                type="date"
                                {...register('dob', { required: t("dobErr") })}
                                className={`input ${focusedInput === 'dob' ? 'input-focus' : ''}`}
                                onFocus={() => setFocusedInput('dob')}
                                onBlur={() => setFocusedInput(null)}
                            />
                            {errors.dob && <p className='error'>{errors.dob.message}</p>}

                        </div>
                        <div className='form-group'>
                            <select
                                {...register('role', { required: t("roleErr") })}
                                className={`input ${focusedInput === 'role' ? 'input-focus' : ''}`}
                                onFocus={() => setFocusedInput('role')}
                                onBlur={() => setFocusedInput(null)}
                            >
                                <option value="">{t("Selecciona tu rol")}</option> {/* Placeholder */}
                                <option value="Administrador">{t("Administrador")}</option>
                                <option value="doctor">{t("Doctor")}</option>
                                <option value="user">{t("Usuario")}</option>
                            </select>
                            {errors.role && <p className='error'>{errors.role.message}</p>}
                        </div>
                    </div>

                        <div className='w-100 d-flex gap-3 justify-content-end'>
                            <Button htmlType="submit" className='w-25 mt-4 blue-btn'>{t('send')}</Button>
                            <Button type="button" className='mt-4 orange-btn' onClick={clear}>{t('clearFields')}</Button>
                        </div>
                </form>
            </div>
        </div>
    );
};

export default RegisterPage;
