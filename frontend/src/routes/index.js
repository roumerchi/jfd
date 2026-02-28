import Contacts from "../pages/Contacts";
import Main from "../pages/Main";
import Auth from "../pages/Auth";

export const publicRotes = [
    {path: "/", component: <Main/>, key: "main"}
]

export const unprivateRotes = [
    {path: "/auth/", component: <Auth/>, key: "auth"}
]

export const privateRotes = [
    {path: "/contacts/", component: <Contacts/>, key: "staff"}
]
