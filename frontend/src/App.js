import AppRouter from "./components/AppRouter";
import {AuthProvider} from "./context";
import {BrowserRouter} from "react-router-dom";
import {createPortal} from "react-dom";
import Header from "./components/Header";
import {Suspense} from "react";
import "./styles/core.css"

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                {createPortal(<Header/>, document.getElementById("header"))}
                <Suspense fallback={null}>
                    <AppRouter/>
                </Suspense>
            </BrowserRouter>
        </AuthProvider>
    )
}


export default App;
