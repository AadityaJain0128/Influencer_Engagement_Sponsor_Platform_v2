<template>
    <div id="container">
        <h1 align="center" class="mb-4">Completed Campaigns</h1>
        <div id="completed_campaigns" class="m-5">
            <table v-if="completed_campaigns.length > 0" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Campaign</th>
                        <th scope="col">Sponsor</th>
                        <th scope="col">Start Date</th>
                        <th scope="col">End Date</th>
                        <th scope="col">Pay Amount</th>
                        <th scope="col">Transaction ID</th>
                        <th scope="col">Paid on</th>
                        <th scope="col">Rating</th>
                        <th scope="col">Campaign Details</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    <tr v-for="campaign in completed_campaigns" :key="campaign.id">
                        <td>{{ campaign.name }}</td>
                        <td>@{{ campaign.sponsor.username }}</td>
                        <td>{{ campaign.start_date }}</td>
                        <td>{{ campaign.end_date }}</td>
                        <td>INR {{ campaign.transaction.amount }}</td>
                        <td>{{ campaign.transaction.id }}</td>
                        <td>{{ campaign.transaction.date }}</td>
                        <td v-if="campaign.rating.rating">{{ campaign.rating.rating }}</td>
                        <td v-else>--</td>
                        <td>
                            <button type="button" class="btn btn-outline-dark" data-bs-toggle="modal" :data-bs-target="'#' + campaign.id">View</button>
                            <div class="modal fade" :id="campaign.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-fullscreen">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Campaign Details</h1>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div v-if="campaign.flagged" id="message" class="mt-5" style="text-align: center; align-content: center;">
                                            <img src="/images/warning.png" width="70px">
                                            <h3>Campaign has been <span class="text-danger">Flagged</span> by Admin !</h3>
                                        </div>
                                        <div class="modal-body d-flex justify-content-center">
                                            <table class="table table-striped mt-5" style="width: 60%;">
                                                <tr>
                                                    <th>Name</th>
                                                    <td>{{ campaign.name }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Description</th>
                                                    <td>{{ campaign.description }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Start Date</th>
                                                    <td>{{ campaign.start_date }}</td>
                                                </tr>
                                                <tr>
                                                    <th>End Date</th>
                                                    <td>{{ campaign.end_date }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Budget</th>
                                                    <td>{{ campaign.budget }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Visibility</th>
                                                    <td>{{ campaign.visibility }}</td>
                                                </tr>
                                            </table>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <span v-else class="text-center d-flex justify-content-center">No completed Campaigns !</span>
        </div>
    </div>
</template>


<script>
    export default {
        name : "InfluencerCampaigns",
        data() {
            return {
                completed_campaigns : [],
            }
        },
        methods : {
            async getCampaigns() {
                let { data } = await this.$http.get("/influencer/completed_campaigns", {
                    headers : { Authorization : `Bearer ${this.$store.getters.authToken}` }
                });

                if (data.status == "success") {
                    this.completed_campaigns = data.completed_campaigns;
                }
            }
        },
        created() {
            this.getCampaigns();
        }
    }
</script>