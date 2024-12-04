<template>
    <div id="container">
        <h1 align="center">Campaign Details</h1>
        <div v-if="campaign.flagged" id="message" class="mt-5" style="text-align: center; align-content: center;">
            <img src="images/warning.png" width="70px">
            <h3>Campaign has been <span class="text-danger">Flagged</span> by Admin !</h3>
            <h6 class="text-muted">Please contact Administrator for more Information.</h6>
        </div>
        <div id="campaign_details" style="width: 30%; float: left;">
            <table class="table table-striped mt-5">
                <tr>
                    <th>Name</th>
                    <td><input type="text" name="name" v-model="cname" class="form-control"></td>
                </tr>
                <tr>
                    <th>Description</th>
                    <td><textarea name="description" class="form-control" rows="5" v-model="description"></textarea></td>
                </tr>
                <tr>
                    <th>Start Date</th>
                    <td><input type="date" name="start_date" v-model="start_date" class="form-control"></td>
                </tr>
                <tr>
                    <th>End Date</th>
                    <td><input type="date" name="end_date" v-model="end_date" class="form-control"></td>
                </tr>
                <tr>
                    <th>Budget (INR)</th>
                    <td><input type="number" step="0.01" name="budget" v-model="budget" class="form-control"></td>
                </tr>
                <tr>
                    <th>Visibility</th>
                    <td>
                        <select name="visibility" class="form-control" v-model="visibility">
                            <option value="public">Public</option>
                            <option value="private">Private</option>
                        </select>
                    </td>
                </tr>
                <tr v-if="campaign.influencer">
                    <th>Influencer</th>
                    <td><input type="text" class="form-control" :value="campaign.influencer.name + '(@' + campaign.influencer.username + ')'" readonly></td>
                </tr>
                <tr v-if="campaign.completed">
                    <th>Paid Amount</th>
                    <td><input type="text" class="form-control" :value="'INR ' + campaign.budget" readonly></td>
                </tr>
                <tr v-if="campaign.rating">
                    <th>Rating</th>
                    <td><input type="text" class="form-control" :value="campaign.rating.rating" readonly></td>
                </tr>
                
                <tr v-if="!campaign.influencer">
                    <td><button @click="updateCampaign" class="btn btn-outline-dark">Save changes</button></td>
                    <td></td>
                </tr>
                <tr v-else-if="!campaign.completed">
                    <td><button @click="markComplete" class="btn btn-outline-dark">Mark as Completed</button></td>
                    <td></td>
                </tr>
                <tr v-else-if="!campaign.rating">
                    <td><button type="button" data-bs-toggle="modal" data-bs-target="#rating" class="btn btn-outline-dark">Rate Influencer</button></td>
                    <td></td>
                </tr>
            </table>
        </div>
        <div>
            <div v-if="campaign.completed" class="modal fade" id="rating" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">Rate Influencer</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <table class="table table-striped mt-3">
                                <tr>
                                    <th>Campaign Name</th>
                                    <td>{{ campaign.name }}</td>
                                </tr>
                                <tr>
                                    <th>Influencer Username</th>
                                    <td>@{{ campaign.influencer.username }}</td>
                                </tr>
                                <tr>
                                    <th>Rating<br>(Between 1 to 5)</th>
                                    <td><input type="number" name="r" min="1" max="5" step=".5" class="form-control" v-model="rating" required></td>
                                </tr>
                            </table>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Discard</button>
                            <button @click="rateInfluencer" class="btn btn-primary">Rate</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id="requests" style="width: 69%; float: right;">
            <div id="recieved_requests" class="m-4 mt-5">
                <h4>Recieved Requests:</h4>
                <table v-if="recieved_requests.length > 0" class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Influencer Name</th>
                            <th scope="col">Username</th>
                            <th scope="col">Messages</th>
                            <th scope="col">Requirements</th>
                            <th scope="col">Pay Amount</th>
                            <th scope="col">Status</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <tr v-for="request in recieved_requests" :key="request.id">
                            <td>{{ request.influencer.name }}</td>
                            <td>@{{ request.influencer.username }}</td>
                            <td>{{ request.messages }}</td>
                            <td>{{ request.requirements }}</td>
                            <td v-if="request.budget == campaign.budget">INR {{ request.budget }}</td>
                            <td v-else-if="request.budget > campaign.budget" style="color: red;">INR {{ request.budget }}</td>
                            <td v-else style="color: green;">INR {{ request.budget }}</td>
                            <td v-if="request.status == 'pending'" style="color: orange;">{{ request.status }}</td>
                            <td v-else-if="request.status == 'accepted'" style="color: green;">{{ request.status }}</td>
                            <td v-else style="color: red;">{{ request.status }}</td>
                            <td v-if="request.status == 'pending'">
                                <button @click="handleRequest(request.id, 'accept')" class="btn btn-outline-success">Accept</button>
                                <button @click="handleRequest(request.id, 'reject')" class="btn btn-outline-danger">Reject</button>
                            </td>
                            <td v-else></td>
                        </tr>
                    </tbody>
                </table>
                <span v-else class="text-muted">Nothing Here !</span>
            </div>
            <div id="sent_requests" class="m-4 mt-5">
                <h4>Sent Requests:</h4>
                <table v-if="sent_requests.length > 0" class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Influencer Name</th>
                            <th scope="col">Username</th>
                            <th scope="col">Messages</th>
                            <th scope="col">Requirements</th>
                            <th scope="col">Pay Amount</th>
                            <th scope="col">Status</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <tr v-for="request in sent_requests" :key="request.id">
                            <td>{{ request.influencer.name }}</td>
                            <td>@{{ request.influencer.username }}</td>
                            <td>{{ request.messages }}</td>
                            <td>{{ request.requirements }}</td>
                            <td>INR {{ request.budget }}</td>
                            <td v-if="request.status == 'pending'" style="color: orange;">{{ request.status }}</td>
                            <td v-else-if="request.status == 'accepted'" style="color: green;">{{ request.status }}</td>
                            <td v-else style="color: red;">{{ request.status }}</td>
                            <td>
                                <img src="images/edit.png" width="20" data-bs-toggle="modal" :data-bs-target="'#edit' + request.id" style="cursor: pointer;">
                                <div class="modal fade" :id="'edit' + request.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                    <div class="modal-dialog modal-lg">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="exampleModalLabel">Request @{{ request.influencer.username }}</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <table class="table table-striped mt-5">
                                                    <tr>
                                                        <th>Messages</th>
                                                        <td><input type="text" name="messages" v-model="messages[request.id]" class="form-control" required></td>
                                                    </tr>
                                                    <tr>
                                                        <th>Requirements</th>
                                                        <td><input type="text" name="requirements" v-model="requirements[request.id]" class="form-control" required></td>
                                                    </tr>
                                                    <tr>
                                                        <th>Pay Amount</th>
                                                        <td><input type="number" step=".01" name="budget" v-model="budgets[request.id]" class="form-control" required></td>
                                                    </tr>
                                                </table>
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                                <button @click="edit_request(request.id)" class="btn btn-primary">Edit Request</button>
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
        </div>
    </div>
</template>


<script>
    export default {
        name : "SponsorCampaignView",
        props : ["id"],
        data() {
            return {
                cname : "",
                description : "",
                start_date : "",
                end_date : "",
                budget : 0,
                visibility : "",
                rating : "",
                sent_requests : [],
                recieved_requests : [],
                campaign : {},
                messages : {},
                requirements : {},
                budgets : {}
            }
        },
        methods : {
            async getCampaignDetails() {
                let { data } = await this.$http.get("/sponsor/campaigns/" + this.id, {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` }
                });

                if (data.status == "success") {
                    this.campaign = data.campaign;
                    this.sent_requests = data.sent_requests;
                    this.recieved_requests = data.recieved_requests;
                    this.cname = this.campaign.name;
                    this.description = this.campaign.description;
                    this.start_date = this.campaign.start_date;
                    this.end_date = this.campaign.end_date;
                    this.budget = this.campaign.budget;
                    this.visibility = this.campaign.visibility;

                    if (this.sent_requests.length > 0) {
                        this.sent_requests.forEach(req => {
                            this.$set(this.messages, req.id, req.messages);
                            this.$set(this.requirements, req.id, req.requirements);
                            this.$set(this.budgets, req.id, req.budget);
                        });
                    }
                } else {
                    this.$store.commit("showAlert", { type : "error", message : data.message });
                    this.$router.push("/campaigns");
                }
            },

            async updateCampaign() {
                let { data } = await this.$http.put("/sponsor/campaigns/" + this.id, {
                    cname : this.cname, description : this.description, start_date : this.start_date,
                    end_date : this.end_date, budget : this.budget, visibility : this.visibility
                },
                { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } });

                if (data.status == "success") {
                    this.$store.commit("showAlert", { type : "success", message : "Campaign has been updated !" });
                    this.getCampaignDetails();
                }
            },

            async markComplete() {
                this.$router.push("/payment_gateway/" + this.id);
            },

            async handleRequest(id, type) {
                let { data } = await this.$http.post("/sponsor/request",
                    { id : id, type : type },
                    { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } }
                );

                if (data.status == "success") {
                    this.getCampaignDetails()
                }
                this.$store.commit("showAlert", { type : data.status, message : data.message });
            },
            async edit_request(id) {
                let { data } = await this.$http.put("/sponsor/request",
                    { id : id, messages : this.messages[id], requirements : this.requirements[id], budget : this.budgets[id] },
                    { headers : { Authorization : `Bearer ${this.$store.getters.authToken}` } }
                );

                if (data.status == "success") {
                    this.$store.commit("showAlert", { type : "success", message : data.message });
                    this.getCampaignDetails();
                } else {
                    this.$store.commit("showAlert", { type : "error", message : data.message });
                }
            },
            async rateInfluencer() {
                let { data } = await this.$http.post("/sponsor/rating",
                    { id : this.id, rating : this.rating },
                    { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } });

                if (data.status == "success") {
                    this.getCampaignDetails();
                }
                this.$store.commit("showAlert", { type : data.status, message : data.message });
                this.rating = "";
            }
        },
        created() {
            this.getCampaignDetails();
        }
    }
</script>