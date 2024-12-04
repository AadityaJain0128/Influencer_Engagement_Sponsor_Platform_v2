<template>
    <InfluencerFind v-if="role == 'influencer'"></InfluencerFind>
    <SponsorFind v-else-if="role == 'sponsor'"></SponsorFind>
</template>


<script>
    import InfluencerFind from './InfluencerFind.vue';
    import SponsorFind from './SponsorFind.vue';

    export default {
        name : "FindPage",
        components : {
            InfluencerFind,
            SponsorFind
        },
        computed : {
            role() {
                return this.$store.state.auth.role;
            }
        }
    }
</script>