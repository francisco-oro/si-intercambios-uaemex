import React from 'react';
import { useNavigate } from 'react-router-dom';
import { setUserRol } from '../../../../../store/slices/globalSlices/generalStates.slice';
import { useDispatch } from 'react-redux';

const Header = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch();

  const log = () => {
    dispatch(setUserRol(''))
    navigate('/login')

  }
  return (
   <div>Header Vendor
 <button onClick={log}>Log in</button>
 <button onClick={() => navigate('/')}>Incio</button>

   </div>
  );
};

export default Header;
