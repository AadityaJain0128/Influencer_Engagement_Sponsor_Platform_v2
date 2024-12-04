<template>
    <div id="container">
        <h1 align="center">Welcome {{ name }}</h1>
        <br><br>
        <div id="active_campaigns" class="m-4 mt-5">
            <h4>Active Campaigns:</h4>
            <table v-if="active_campaigns.length > 0" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Start Date</th>
                        <th scope="col">End Date</th>
                        <th scope="col">Budget</th>
                        <th scope="col">Visibility</th>
                        <th scope="col">Influencer</th>
                        <th scope="col">Details</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    <tr v-for="campaign in active_campaigns" :key="campaign.id">
                        <td>{{ campaign.name }}</td>
                        <td>{{ campaign.start_date }}</td>
                        <td>{{ campaign.end_date }}</td>
                        <td>INR {{ campaign.budget }}</td>
                        <td>{{ campaign.visibility }}</td>
                        <td>{{ campaign.influencer.name }}(@{{ campaign.influencer.username }})</td>
                        <td><router-link :to="'/campaigns/' + campaign.id" class="btn btn-outline-dark">View</router-link></td>
                    </tr>
                </tbody>
            </table>
            <span v-else class="text-muted">Nothing Here !</span>
        </div>
        <div id="recieved_requests" class="m-4 mt-5">
            <h4>Recieved Requests:</h4>
            <table v-if="recieved_requests.length > 0" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Influencer Name</th>
                        <th scope="col">Influencer Username</th>
                        <th scope="col">Messages</th>
                        <th scope="col">Requirements</th>
                        <th scope="col">Budget</th>
                        <th scope="col">Pay Amount</th>
                        <th scope="col">Status</th>
                        <th scope="col">Details</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    <tr v-for="request in recieved_requests" :key="request.id">
                        <td>{{ request.influencer.name }}</td>
                        <td>@{{ request.influencer.username }}</td>
                        <td>{{ request.messages }}</td>
                        <td>{{ request.requirements }}</td>
                        <td>INR {{ request.campaign.budget }}</td>
                        <td v-if="request.budget == request.campaign.budget">INR {{ request.budget }}</td>
                        <td v-else-if="request.budget > request.campaign.budget" style="color: red;">INR {{ request.budget }}</td>
                        <td v-else style="color: green;">INR {{ request.budget }}</td>
                        <td v-if="request.status == 'pending'" style="color: orange;">{{ request.status }}</td>
                        <td v-else-if="request.status == 'accepted'" style="color: green;">{{ request.status }}</td>
                        <td v-else style="color: red;">{{ request.status }}</td>
                        <td><router-link :to="'/campaigns/' + request.campaign.id" class="btn btn-outline-dark">View</router-link></td>
                        <td>
                            <button @click="handleRequest(request.id, 'accept')" class="btn btn-outline-success">Accept</button>
                            <button @click="handleRequest(request.id, 'reject')" class="btn btn-outline-danger">Reject</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <span v-else class="text-muted">Nothing Here !</span>
        </div>
    </div>
</template>


<script>
    export default {
        name : "SponsorDashboard",
        data() {
            return {
                active_campaigns : [],
                recieved_requests : []
            }
        },
        methods : {
            async getDetails() {
                let { data } = await this.$http.get("/sponsor/getDetails", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` }
                });

                if (data.status == "success") {
                    this.$store.commit("setInfo", { id : data.id, name : data.name, category : data.category, reach : 0, socials : {} });
                }
            },

            async dashBoard() {
                let { data } = await this.$http.get("/sponsor/dashboard", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` }
                });

                if (data.status == "success") {
                    this.active_campaigns = data.active_campaigns;
                    this.recieved_requests = data.recieved_requests;
                }
            },

            async handleRequest(id, type) {
                let { data } = await this.$http.post("/sponsor/request",
                    { id : id, type : type },
                    { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } }
                );

                if (data.status == "success") {
                    this.dashBoard()
                }
                this.$store.commit("showAlert", { type : data.status, message : data.message });
            }
        },
        computed : {
            name() {
                return this.$store.state.info.name;
            }
        },
        created() {
            this.getDetails();
            this.dashBoard();
        }
    }
</script>