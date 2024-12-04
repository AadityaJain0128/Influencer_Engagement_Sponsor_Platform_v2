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
                <router-link class="nav-link" to="/campaigns">Campaigns</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/find">Find</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/transactions">Transactions</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/stats">Stats</router-link>
                </li>
                <li class="nav-item ms-2 me-2">
                <router-link class="nav-link" to="/profile">Profile</router-link>
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
        name : "SponsorNavbar",
        methods : {
            logOut() {
                this.$store.commit("logOut");
                this.$store.commit("dismissAlert");
                this.$router.push("/login");
            }
        }
    }
</script>