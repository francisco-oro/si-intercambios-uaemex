import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useDispatch, useSelector } from 'react-redux';
import { Button } from 'antd';
import { useTranslation } from 'react-i18next';
import { addClinicThunk } from '../../../../../../store/slices/Admin/customers/customers-vendorsModule.slice';

const UsersForm = ({ onClose }) => {
    const { t } = useTranslation('admin')
    const isDesktop = useSelector(state => state.generalStates.isDesktopSize);
    const { register, handleSubmit, formState: { errors }, reset } = useForm();
    const dispatch = useDispatch();

    const [focusedInput, setFocusedInput] = useState(null);

    const onSubmit = ({ name, address, email, phone, website }) => {
        const clinicAddMsg = t("newClinicMsg")
        const clinicData = {
            name,
            address,
            email,
            phone,
            website
        };
        reset();
        dispatch(addClinicThunk(clinicData, clinicAddMsg));
        onClose();
        // console.log(clinicData)
    };
    const clear = () => {
        reset()
    }

    return (
        <div>
            <form onSubmit={handleSubmit(onSubmit)} className='form-container'>
                {/* Nombre */}
                <div className={isDesktop ? 'd-flex w-100 gap-3' : 'w-100'}>
                    <div className='form-group'>
                        <input
                            type="text"
                            placeholder={t("clinicName")}
                            {...register('name', { required: t("clinicNameErr") })}
                            className={`input ${focusedInput === 'name' ? 'input-focus' : ''}`}
                            onFocus={() => setFocusedInput('name')}
                            onBlur={() => setFocusedInput(null)}
                        />
                        {errors.name && <p className='error'>{errors.name.message}</p>}
                    </div>

                    {/* Apellido */}
                    <div className='form-group'>
                        <input
                            type="text"
                            placeholder={t("clinicAddress")}
                            {...register('address', { required: t("clinicAddressErr") })}
                            className={`input ${focusedInput === 'address' ? 'input-focus' : ''}`}
                            onFocus={() => setFocusedInput('address')}
                            onBlur={() => setFocusedInput(null)}
                        />
                        {errors.address && <p className='error'>{errors.address.message}</p>}
                    </div>
                </div>

                {/* Correo electrónico y Contraseña */}
                <div className={isDesktop ? 'd-flex w-100 gap-3' : 'w-100'}>
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
                            type="text"
                            placeholder={t("number")}
                            {...register('phone', { required: t("clinicPhoneErr") })}
                            className={`input ${focusedInput === 'phone' ? 'input-focus' : ''}`}
                            onFocus={() => setFocusedInput('phone')}
                            onBlur={() => setFocusedInput(null)}
                        />
                        {errors.phone && <p className='error'>{errors.phone.message}</p>}
                    </div>
                </div>

                {/* Fecha de nacimiento */}
                <div className='form-group'>
                    <input
                        type="text"
                        placeholder={t("websiteLink")}
                        {...register('website', { required: t("clinicWebsite") })}
                        className={`input ${focusedInput === 'website' ? 'input-focus' : ''}`}
                        onFocus={() => setFocusedInput('website')}
                        onBlur={() => setFocusedInput(null)}
                    />
                    {errors.website && <p className='error'>{errors.website.message}</p>}
                </div>

                <div className='w-100 d-flex gap-3 justify-content-end'>
                    <Button htmlType="submit" className='w-25 mt-4 blue-btn'>{t('sendData')}</Button>
                    <Button type="button" className='mt-4 orange-btn' onClick={clear}>{t('clearFields')}</Button>
                </div>

            </form>

        </div>
    );
};

export default UsersForm;
