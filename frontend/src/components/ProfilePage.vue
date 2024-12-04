<template>
    <InfluencerProfile v-if="role == 'influencer'"></InfluencerProfile>
    <SponsorProfile v-else-if="role == 'sponsor'"></SponsorProfile>
</template>

<script>
    import InfluencerProfile from './InfluencerProfile.vue';
    import SponsorProfile from './SponsorProfile.vue';

    export default {
        name : "ProfilePage",
        components : {
            InfluencerProfile,
            SponsorProfile
        },
        computed : {
            role() { return this.$store.state.auth.role }
        }
    }
</script>