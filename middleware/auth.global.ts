export default defineNuxtRouteMiddleware((to, from) => {
    console.log("from", from.fullPath, "to", to.fullPath);
    const isAuthenticated = useAuthentication()
    if (isAuthenticated) {
        return;
    }

    if (to.fullPath !== "/login" && to.fullPath !== "/") {
        console.log("redirected to /login");
        return navigateTo("/login");
    }
});