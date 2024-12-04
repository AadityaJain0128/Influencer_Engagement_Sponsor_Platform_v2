<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/">IESCP</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/verify_sponsors">Verify Sponsors</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/find_campaigns">Flag Campaigns</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/flagged_campaigns">Flagged Campaigns</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/find_users">Flag Users</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/flagged_users">Flagged Users</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <button class="nav-link" @click="logOut">Logout</button>
                </li>
            </ul>
            </div>
        </div>
    </nav>
</template>


<script>
    export default {
        name : "AdminNavbar",
        methods : {
            logOut() {
                this.$store.commit("logOut");
                this.$store.commit("dismissAlert");
                this.$router.push("/login");
            }
        }
    }
</script>