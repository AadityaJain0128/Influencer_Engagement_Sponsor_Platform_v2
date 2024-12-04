<template>
    <InfluencerStats v-if="role == 'influencer'"></InfluencerStats>
    <SponsorStats v-else-if="role == 'sponsor'"></SponsorStats>
</template>

<script>
    import InfluencerStats from './InfluencerStats.vue';
    import SponsorStats from './SponsorStats.vue';

    export default {
        name : "StatsPage",
        components : {
            InfluencerStats,
            SponsorStats
        },
        computed : {
            role() {
                return this.$store.state.auth.role;
            }
        }
    }
</script>