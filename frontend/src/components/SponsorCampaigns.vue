<template>
    <div id="container">
        <h1 align="center">Add Campaign</h1>
        <br>
        <div id="add_campaign" class="d-flex justify-content-center">
            <a type="button" data-bs-toggle="modal" data-bs-target="#add">
                <img src="images/add.png" height="60px" width="60px">
            </a>
            <div class="modal fade" id="add" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-fullscreen">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">Add Campaign</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <span v-if="error" class="text-center d-flex justify-content-center" style="color: red;">{{ error }}</span>
                            <span v-if="message" class="text-center d-flex justify-content-center" style="color: green;">{{ message }}</span>
                            <br>
                            <table class="table table-striped mt-5" style="width: 60%; margin: auto;">
                                <tr>
                                    <th>Name</th>
                                    <td><input type="text" name="name" class="form-control" v-model="cname"></td>
                                </tr>
                                <tr>
                                    <th>Description</th>
                                    <td><textarea name="description" class="form-control" rows="8" v-model="description"></textarea></td>
                                </tr>
                                <tr>
                                    <th>Start Date</th>
                                    <td><input type="date" name="start_date" class="form-control" v-model="start_date"></td>
                                </tr>
                                <tr>
                                    <th>End Date</th>
                                    <td><input type="date" name="end_date" class="form-control" v-model="end_date"></td>
                                </tr>
                                <tr>
                                    <th>Budget</th>
                                    <td><input type="number" step="0.01" name="budget" class="form-control" v-model="budget"></td>
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
                            </table>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Discard</button>
                            <button type="submit" class="btn btn-primary" @click="addCampaign">Add Campaign</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <br>
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
                        <td>@{{ campaign.influencer.username }}</td>
                        <td><router-link :to="'/campaigns/' + campaign.id" class="btn btn-outline-dark">View</router-link></td>
                    </tr>
                </tbody>
            </table>
            <span v-else class="text-muted">Nothing Here !</span>
        </div>
        <div id="pending_campaigns" class="m-4 mt-5">
            <h4>Pending Campaigns:</h4>
            <table v-if="pending_campaigns.length > 0" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Start Date</th>
                        <th scope="col">End Date</th>
                        <th scope="col">Budget</th>
                        <th scope="col">Visibility</th>
                        <th scope="col">Details</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    <tr v-for="campaign in pending_campaigns" :key="campaign.id">
                        <td>{{ campaign.name }}</td>
                        <td>{{ campaign.start_date }}</td>
                        <td>{{ campaign.end_date }}</td>
                        <td>INR {{ campaign.budget }}</td>
                        <td>{{ campaign.visibility }}</td>
                        <td><router-link :to="'/campaigns/' + campaign.id" class="btn btn-outline-dark">View</router-link></td>
                        <td><button @click="deleteCampaign(campaign.id)" class="btn btn-outline-danger">Delete</button></td>
                    </tr>
                </tbody>
            </table>
            <span v-else class="text-muted">Nothing Here !</span>
        </div>
        <div id="completed_campaigns" class="m-4 mt-5">
            <h4>Completed Campaigns:</h4>
            <table v-if="completed_campaigns.length > 0" class="table table-striped">
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
                    <tr v-for="campaign in completed_campaigns" :key="campaign.id">
                        <td>{{ campaign.name }}</td>
                        <td>{{ campaign.start_date }}</td>
                        <td>{{ campaign.end_date }}</td>
                        <td>INR {{ campaign.budget }}</td>
                        <td>{{ campaign.visibility }}</td>
                        <td>@{{ campaign.influencer.username }}</td>
                        <td><router-link :to="'/campaigns/' + campaign.id" class="btn btn-outline-dark">View</router-link></td>
                    </tr>
                </tbody>
            </table>
            <span v-else class="text-muted">Nothing Here !</span>
        </div>
    </div>
</template>


<script>
    export default {
        name : "SponsorCampaigns",
        data() {
            return {
                cname : "",
                description : "",
                start_date : "",
                end_date : "",
                budget : "",
                visibility : "",
                active_campaigns : [],
                pending_campaigns : [],
                completed_campaigns : [],
                error : "",
                message : ""
            }
        },
        methods : {
            async getCampaigns() {
                let { data } = await this.$http.get("/sponsor/getCampaigns", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` }
                });

                if (data.status == "success") {
                    this.active_campaigns = data.active_campaigns;
                    this.pending_campaigns = data.pending_campaigns;
                    this.completed_campaigns = data.completed_campaigns;
                }
            },
            async addCampaign() {
                if (this.cname == "" || this.description == "" || this.start_date == "" || this.end_date == "" || this.budget == "" || this.visibility == "") {
                    this.error = "* Please fill out all the fields first !";
                    return;
                }

                let { data } = await this.$http.post("/sponsor/addCampaign", {
                    name : this.cname, description : this.description, start_date : this.start_date, end_date : this.end_date, budget : this.budget, visibility : this.visibility
                }, {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` }
                });

                if (data.status == "success") {
                    this.cname = ""; this.description = ""; this.start_date = ""; this.end_date = ""; this.budget = ""; this.visibility = "";
                    this.message = "Campaign has been added !";
                }
                this.getCampaigns();
            },
            async deleteCampaign(id) {
                let { data } = await this.$http.delete("/sponsor/campaigns/" + id,
                    { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } }
                );

                if (data.status == "success") {
                    this.$store.commit("showAlert", { type : data.status, message : data.message });
                    this.getCampaigns();
                }
            }
        },
        created() {
            this.getCampaigns();
        }
    }
</script>