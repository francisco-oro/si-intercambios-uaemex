import React from 'react';
import { useNavigate } from 'react-router-dom';
import { setUserRol } from '../../../../../store/slices/globalSlices/generalStates.slice';
import { useDispatch, useSelector } from 'react-redux';
import { Button } from 'antd';

const Header = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch();
  const isAuthenticated = useSelector(state => state.authentication.isAuthenticated)
  const log = () => {
    dispatch(setUserRol(''))
    navigate('/login')

  }
  return (
   <div>
    Header Customer

    <button onClick={log}>Log in</button>
    <button onClick={() => navigate('/')}>Incio</button>
    {
      isAuthenticated? (
        <>
          <Button onClick={() => navigate('/admin')}> Admin </Button>
        </>
      ): (<>:</>)
    }
   </div>

   
  );
};

export default Header;
