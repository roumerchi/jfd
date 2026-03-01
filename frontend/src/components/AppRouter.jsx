import {Navigate, Route, Routes} from "react-router-dom";
import {privateRotes, publicRotes, unprivateRotes} from "../routes";
import {useAuth} from "../context";
import {useEffect, useState} from "react";

const AppRouter = () => {
    const { isAuth, setIsAuth, refreshAccessToken } = useAuth();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const checkToken = async () => {
            const refreshToken = localStorage.getItem('token');
            if (refreshToken) {
                try {
                    const access = await refreshAccessToken();
                    if (access) {
                        setIsAuth(true);
                    } else {
                        setIsAuth(false);
                    }
                } catch (e) {
                    setIsAuth(false);
                }
            }
            setIsLoading(false);
        };
        void checkToken();
    }, []);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <Routes>
            {isAuth ? (
                privateRotes.map(route =>
                    <Route path={route.path} element={route.component} key={route.key}></Route>
                )
            ) : (
                unprivateRotes.map(route =>
                    <Route path={route.path} element={route.component} key={route.key}></Route>
                )
            )}
            {publicRotes.map(route =>
                    <Route path={route.path} element={route.component} key={route.key}></Route>
            )}
            <Route path="*" element={<Navigate to="/" replace />} key={"redirect"}/>
        </Routes>
    );
};

export default AppRouter;