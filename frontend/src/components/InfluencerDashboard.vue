<template>
    <div id="container">
        <h1 align="center">Welcome {{ name.split(" ")[0] }}</h1>
        <div style="width: 20%; float: left;" class="m-4">
            <div align="center">
                <div id="earnings">
                    <table class="table" style="width: 18rem;">
                        <thead><h4 align="left" class="ms-2">Earnings</h4></thead>
                        <tbody>
                            <tr>
                                <th>This month</th>
                                <td>INR {{ month_earnings }}</td>
                            </tr>
                            <tr>
                                <th>Total</th>
                                <td>INR {{ total_earnings }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="card" style="width: 18rem; align-items: center; text-align: center;">
                    <img :src="this.$store.state.auth.profile" width="200px" height="200px" class="mt-2" style="border-radius: 50%; object-fit: cover;" loading="lazy">
                    <div class="card-body">
                        <h5 class="card-title">{{ name }}</h5>
                        <p class="card-text">@{{ username }}</p>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Niche: {{ category }}</li>
                        <li v-if="avg_rating.length == 0" class="list-group-item">Rating: N/A <span class="text-muted" style="font-size: smaller;">(0)</span></li>
                        <li v-else class="list-group-item">Rating: {{ avg_rating[0] }} <span class="text-muted" style="font-size: smaller;">({{ avg_rating[1] }})</span></li>
                        <li class="list-group-item">Reach: {{ reach }}</li>
                        <li class="list-group-item">
                            Active Socials<br>
                            <span v-if="reach == 0" class="text-muted">No Socials added !</span>
                            <span v-else>
                                <img v-for="[social, ] in Object.entries(socials)" :key="social" :src="'/images/' + social + '.png'" width="30px" class="m-1 mt-2">
                            </span>
                        </li>
                    </ul>
                </div>
                <span class="text-muted">This profile is visible to the sponsors.</span>
            </div>
        </div>
        <div style="width: 75%; float: right;" class="mt-5">
            <div id="active_campaigns">
                <h4>Active Campaigns:</h4>
                <table v-if="active_campaigns.length > 0" class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Campaign</th>
                            <th scope="col">Sponsor</th>
                            <th scope="col">Start Date</th>
                            <th scope="col">End Date</th>
                            <th scope="col">Pay Amount</th>
                            <th scope="col">Visibility</th>
                            <th scope="col">Details</th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <tr v-for="campaign in active_campaigns" :key="campaign.id">
                            <td>{{ campaign.name }}</td>
                            <td>{{ campaign.sponsor.name }}</td>
                            <td>{{ campaign.start_date }}</td>
                            <td>{{ campaign.end_date }}</td>
                            <td>INR {{ campaign.budget }}</td>
                            <td>{{ campaign.visibility }}</td>
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
                <span v-else class="text-muted">Nothing Here !</span>
            </div>
            <br>
            <div id="recieved_requests">
                <h4>Recieved Requests:</h4>
                <table v-if="recieved_requests.length > 0" class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Campaign</th>
                            <th scope="col">Sponsor</th>
                            <th scope="col">Messages</th>
                            <th scope="col">Requirements</th>
                            <th scope="col">Pay Amount</th>
                            <th scope="col">Status</th>
                            <th scope="col">Details</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <tr v-for="request in recieved_requests" :key="request.id">
                            <td>{{ request.campaign.name }}</td>
                            <td>{{ request.sponsor.name }}</td>
                            <td>{{ request.messages }}</td>
                            <td>{{ request.requirements }}</td>
                            <td>INR {{ request.budget }}</td>
                            <td v-if="request.status == 'pending'" style="color: orange;">{{ request.status }}</td>
                            <td v-else-if="request.status == 'accepted'" style="color: green;">{{ request.status }}</td>
                            <td v-else style="color: red;">{{ request.status }}</td>
                            <td>
                                <button type="button" class="btn btn-outline-dark" data-bs-toggle="modal" :data-bs-target="'#' + request.campaign.id">View</button>
                                <div class="modal fade" :id="request.campaign.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                    <div class="modal-dialog modal-fullscreen">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="exampleModalLabel">Campaign Details</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div v-if="request.campaign.flagged" id="message" class="mt-5" style="text-align: center; align-content: center;">
                                                <img src="/images/warning.png" width="70px">
                                                <h3>Campaign has been <span class="text-danger">Flagged</span> by Admin !</h3>
                                            </div>
                                            <div class="modal-body d-flex justify-content-center">
                                                <table class="table table-striped mt-5" style="width: 60%;">
                                                    <tr>
                                                        <th>Name</th>
                                                        <td>{{ request.campaign.name }}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Description</th>
                                                        <td>{{ request.campaign.description }}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Start Date</th>
                                                        <td>{{ request.campaign.start_date }}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>End Date</th>
                                                        <td>{{ request.campaign.end_date }}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Budget</th>
                                                        <td>{{ request.campaign.budget }}</td>
                                                    </tr>
                                                    <tr>
                                                        <th>Visibility</th>
                                                        <td>{{ request.campaign.visibility }}</td>
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
                            <td>
                                <a class="btn btn-outline-success" @click="handle_request(request.id, 'accepted')">Accept</a>
                                <a class="btn btn-outline-danger" @click="handle_request(request.id, 'rejected')">Reject</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <span v-else class="text-muted">Nothing Here !</span>
            </div>
        </div>
    </div>
</template>


<script>
    export default {
        name : "InfluencerDashboard",
        data() {
            return {
                active_campaigns : [],
                recieved_requests : [],
                avg_rating : [],
                month_earnings : null,
                total_earnings : null
            }
        },
        methods : {
            async getDetails() {
                let response = await this.$http.get("/influencer/getDetails", {
                    headers : { "Authorization" : `Bearer ${this.$store.getters.authToken}` }
                });
                if (response.data.status == "fail") {
                    this.$store.commit("showAlert", { type : "error", message : response.data.error });
                } else {
                    this.$store.commit("setInfo", { id : response.data.id, name : response.data.name, category : response.data.category, reach : response.data.reach, socials : response.data.socials });
                }
            },

            async dashboard() {
                let { data } = await this.$http.get("/influencer/dashboard", {
                    headers : { "Authorization" : `Bearer ${this.$store.getters.authToken}` }
                });
                if (data.status == "fail") {
                    this.$store.commit("showAlert", { type : "error", message : data.error });
                } else {
                    this.active_campaigns = data.active_campaigns;
                    this.recieved_requests = data.recieved_requests;
                    this.avg_rating = data.avg_rating;
                    this.month_earnings = data.month_earnings;
                    this.total_earnings = data.total_earnings;
                }
            },

            async handle_request(id, action) {
                let { data } = await this.$http.post("/influencer/handle_request",
                    { id : id, action : action },
                    { headers : { "Authorization" : `Bearer ${this.$store.getters.authToken}` }}
                );

                if (data.status == "fail") {
                    this.$store.commit("showAlert", { type : "error", message : data.message });
                } else {
                    this.$store.commit("showAlert", { type : "success", message : data.message });
                }
                this.dashboard();
            }
        },
        computed : {
            username() {
                return this.$store.state.auth.username;
            },
            id() {
                return this.$store.state.info.id;
            },
            name() {
                return this.$store.state.info.name;
            },
            category() {
                return this.$store.state.info.category;
            },
            reach() {
                return this.$store.state.info.reach;
            },
            socials() {
                return Object.entries(this.$store.state.info.socials).filter(([, followers]) => followers > 0).reduce((acc, [social, followers]) => {
                    acc[social] = followers;
                    return acc;
                }, {});
            }
        },
        created() {
            this.getDetails();
            this.dashboard();
        }
    }
</script>