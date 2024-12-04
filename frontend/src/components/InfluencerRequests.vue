<template>
    <div id="container">
        <h1 align="center">Requests</h1>
        <div id="recieved_requests" class="m-4 mt-5">
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
                        <td>{{ request.sponsor.username }}</td>
                        <td>{{ request.messages }}</td>
                        <td>{{ request.requirements }}</td>
                        <td>INR {{ request.budget }}</td>
                        <td v-if='request.status == "pending"' style="color: orange;">{{ request.status }}</td>
                        <td v-else-if='request.status == "accepted"' style="color: green;">{{ request.status }}</td>
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
                        <td v-if="request.status == 'pending'">
                            <button class="btn btn-outline-success" @click="handle_request(request.id, 'accepted')">Accept</button>
                            <button class="btn btn-outline-danger" @click="handle_request(request.id, 'rejected')">Reject</button>
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
                        <th scope="col">Campaign</th>
                        <th scope="col">Sponsor</th>
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
                    <tr v-for="request in sent_requests" :key="request.id">
                        <td>{{ request.campaign.name }}</td>
                        <td>@{{ request.sponsor.username }}</td>
                        <td>{{ request.messages }}</td>
                        <td>{{ request.requirements }}</td>
                        <td>INR {{ request.campaign.budget }}</td>
                        <td v-if="request.budget == request.campaign.budget">INR {{ request.budget }}</td>
                        <td v-else-if="request.budget > request.campaign.budget" style="color: green;">INR {{ request.budget }}</td>
                        <td v-else style="color: red;">INR {{ request.budget }}</td>
                        <td v-if='request.status == "pending"' style="color: orange;">{{ request.status }}</td>
                        <td v-else-if='request.status == "accepted"' style="color: green;">{{ request.status }}</td>
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
                            <img v-if="request.status == 'pending'" src="/images/edit.png" width="20px" data-bs-toggle="modal" :data-bs-target="'#edit' + request.id" style="cursor: pointer;">
                            <div class="modal fade" :id="'edit' + request.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-lg">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Request @{{ request.sponsor.username }}</h1>
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
</template>

<script>
    export default {
        name : "InfluencerRequests",
        data() {
            return {
                recieved_requests : [],
                sent_requests : [],
                messages : {},
                requirements : {},
                budgets : {}
            }
        },

        methods : {
            async fetchRequests() {
                let { data } = await this.$http.get("/influencer/get_requests", {
                    headers : { Authorization : `Bearer ${this.$store.getters.authToken}` }
                });

                if (data.status == "fail") {
                    this.$store.commit("showAlert", { type : "error", message : data.error });
                } else {
                    this.recieved_requests = data.recieved_requests;
                    this.sent_requests = data.sent_requests;
                    
                    if (this.sent_requests.length > 0) {
                        this.sent_requests.forEach(req => {
                            this.$set(this.messages, req.id, req.messages);
                            this.$set(this.requirements, req.id, req.requirements);
                            this.$set(this.budgets, req.id, req.budget);
                        });
                    }
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
                this.fetchRequests();
            },
            async edit_request(id) {
                let { data } = await this.$http.put("/influencer/handle_request",
                    { id : id, messages : this.messages[id], requirements : this.requirements[id], budget : this.budgets[id] },
                    { headers : { Authorization : `Bearer ${this.$store.getters.authToken}` } }
                );

                if (data.status == "success") {
                    this.$store.commit("showAlert", { type : "success", message : data.message });
                    this.fetchRequests();
                } else {
                    this.$store.commit("showAlert", { type : "error", message : data.message });
                }
            }
        },
        created() {
            this.fetchRequests();
        }
    }
</script>