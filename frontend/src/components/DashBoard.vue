<template>
    <AdminDashboard v-if="role == 'admin'"></AdminDashboard>
    <InfluencerDashboard v-else-if="role == 'influencer'"></InfluencerDashboard>
    <SponsorDasboard v-else></SponsorDasboard>
</template>


<script>
    import AdminDashboard from './AdminDashboard.vue';
    import InfluencerDashboard from './InfluencerDashboard.vue';
    import SponsorDasboard from './SponsorDasboard.vue';


    export default {
        name : "DashBoard",
        components : {
            AdminDashboard,
            InfluencerDashboard,
            SponsorDasboard
        },
        computed : {
            role() {
                return this.$store.state.auth.role;
            }
        }
    }
</script>