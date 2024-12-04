<template>
    <div id="container">
        <h1 align="center">Find Campaigns</h1>
        <br><br>
        <div style="width: 20%; float: left;" class="m-3">
            <h3>Filters</h3>
            <br>
            <label for="cname" class="form-label">Campaign Name</label>
            <input v-model="cname" type="text" id="cname" name="cname" placeholder="Search by Campaign Name" class="form-control">
            <br>
            <label for="sname" class="form-label">Sponsor Name</label>
            <input v-model="sname" type="text" id="sname" name="sname" placeholder="Search by Sponsor Name" class="form-control">
            <br>
            <button type="submit" class="btn btn-outline-dark" @click="get_campaigns">Search</button>
        </div>
        <div style="width: 65%; float: right;" class="me-5">
            <div v-if="campaigns.length > 0" class="row">
                <div v-for="c in campaigns" :key="c.id" class="col-md-4 mb-5">
                    <div class="card" style="width: 18rem; align-items: center; text-align: center;">
                        <div class="card-body">
                            <h3 class="card-title">{{ c.name }}</h3>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">Description: {{ c.description }}</li>
                            <li class="list-group-item">Sponsor: {{ c.sponsor.name }}</li>
                            <li class="list-group-item">Industry: {{ c.sponsor.industry }}</li>
                            <li class="list-group-item">Start Date: {{ c.start_date }}</li>
                            <li class="list-group-item">End date: {{ c.end_date }}</li>
                            <li class="list-group-item">Budget: INR {{ c.budget }}</li>
                        </ul>
                        <div class="card-body">
                            <button type="button" class="btn btn-outline-dark" data-bs-toggle="modal" :data-bs-target="'#' + c.id">Send Request</button>
                            <div class="modal fade" :id="c.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-lg">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Request Campaign</h1>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <table class="table table-striped mt-5">
                                                <thead><h4>{{ c.name }}</h4></thead>
                                                <tbody>
                                                    <tr>
                                                        <th>Messages</th>
                                                        <td><input type="text" name="messages" class="form-control" required v-model="messages[c.id]"></td>
                                                    </tr>
                                                    <tr>
                                                        <th>Requirements</th>
                                                        <td><input type="text" name="requirements" class="form-control" v-model="requirements[c.id]" required></td>
                                                    </tr>
                                                    <tr>
                                                        <th>Budget</th>
                                                        <td><input type="text" name="budget" class="form-control" :value="c.budget" readonly></td>
                                                    </tr>
                                                    <tr>
                                                        <th>Negotiation Amount</th>
                                                        <td><input type="number" step=".01" name="req_budget" class="form-control" v-model="neg_budgets[c.id]" required></td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                            <button type="submit" class="btn btn-primary" @click="send_request(c.id)">Send Request</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else style="margin: 130px 0 0 220px;">
                <span>No Results found !</span>
                <br><br>
                <button @click="clearFilters" class="btn btn-outline-secondary">Clear all filters</button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name : "InfluencerFind",
        data() {
            return {
                campaigns : [],
                cname : "",
                sname : "",
                messages : {},
                requirements : {},
                neg_budgets : {}
            }
        },
        methods : {
            async get_campaigns() {
                let { data } = await this.$http.get("/influencer/get_campaigns", {
                    headers : { Authorization : `Bearer ${this.$store.getters.authToken}` },
                    params : { cname : this.cname, sname : this.sname }
                });

                if (data.status == "success") {
                    this.campaigns = data.campaigns;

                    this.campaigns.forEach(c => {
                        this.$set(this.neg_budgets, c.id, c.budget);
                        this.$set(this.messages, c.id, "");
                        this.$set(this.requirements, c.id, "");
                    });
                }
            },
            async send_request(id) {
                let { data } = await this.$http.post("/influencer/send_request",
                    { campaign_id : id, messages : this.messages[id], requirements : this.requirements[id], neg_budget : this.neg_budgets[id] },
                    { headers : { Authorization : `Bearer ${this.$store.getters.authToken}` } }
                );

                let type = data.status == "fail" ? "warning" : "success";
                this.$store.commit("showAlert", { type : type, message : data.message });

                this.$set(this.messages, id, "");
                this.$set(this.requirements, id, "");
                this.$set(this.neg_budgets, id, this.campaigns.find(c => c.id === id).budget);
            },
            clearFilters() {
                this.cname = "";
                this.sname = "";
                this.get_campaigns();
            }
        },
        created() {
            this.get_campaigns();
        }
    }
</script>