<template>
    <InfluencerNavbar v-if="role == 'influencer'"></InfluencerNavbar>
    <SponsorNavbar v-else-if="role == 'sponsor'"></SponsorNavbar>
    <AdminNavbar v-else-if="role == 'admin'"></AdminNavbar>
</template>

<script>
    import AdminNavbar from './AdminNavbar.vue';
    import InfluencerNavbar from './InfluencerNavbar.vue';
    import SponsorNavbar from './SponsorNavbar.vue';

    export default {
        name : "NavBar",
        components : {
            InfluencerNavbar,
            SponsorNavbar,
            AdminNavbar
        },
        computed : {
            role() {
                return this.$store.state.auth.role;
            }
        }
    }
</script>