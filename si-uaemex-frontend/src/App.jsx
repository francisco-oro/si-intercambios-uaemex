import { useEffect, useState } from "react";
import Router from "./router/Router";
import { useDispatch } from "react-redux";
import { setIsDesktopSize } from "./store/slices/globalSlices/generalStates.slice";

function App() {

  const [isDesktop, setIsDesktop] = useState(window.innerWidth >= 1024);
  const dispatch = useDispatch();


  useEffect(() => {
    const handleResize = () => {
      const isDesktop = window.innerWidth >= 1024; 
      setIsDesktop(isDesktop);
      dispatch(setIsDesktopSize(isDesktop));
    };

    handleResize();

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [dispatch]);

  return (
    <>
      <div>
        <Router/>
      </div>
    </>
  )
}

export default App
