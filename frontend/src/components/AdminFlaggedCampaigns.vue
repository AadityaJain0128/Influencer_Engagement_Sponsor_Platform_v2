<template>
    <div id="container">
        <h1 align="center">Flagged Campaigns</h1>
        <br><br>
        <div style="width: 20%; float: left;" class="m-3">
            <h3>Filters</h3>
            <br>
            <label for="cname" class="form-label">Campaign Name</label>
            <input type="text" id="cname" name="cname" placeholder="Search by Campaign Name" v-model="cname" class="form-control">
            <br>
            <label for="sname" class="form-label">Sponsor Name</label>
            <input type="text" id="sname" name="sname" placeholder="Search by Sponsor Name" v-model="sname" class="form-control">
            <br>
            <button @click="getCampaigns" class="btn btn-outline-dark">Search</button>
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
                            <li class="list-group-item">Visibility: {{ c.visibility }}</li>
                            <li v-if="c.influencer" class="list-group-item">Status: Active</li>
                            <li v-if="c.influencer" class="list-group-item">Influencer: @{{ c.influencer.username }}</li>
                            <li v-else class="list-group-item">Status: Pending</li>
                        </ul>
                        <div class="card-body">
                            <button @click="unflagCampaign(c.id)" class="btn btn-outline-success">UnFlag Campaign</button>
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
        name : "AdminFlaggedCampaigns",
        data() {
            return {
                cname : "",
                sname : "",
                campaigns : []
            }
        },
        methods : {
            async getCampaigns() {
                let { data } = await this.$http.get("/admin/flagged_campaigns", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` },
                    params : { cname : this.cname, sname : this.sname }
                });
                if (data.status == "success") {
                    this.campaigns = data.campaigns;
                }
            },
            async unflagCampaign(id) {
                let { data } = await this.$http.post("/admin/flagged_campaigns",
                    { id : id },
                    { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } }
                );
                if (data.status == "success") {
                    this.$store.commit("showAlert", { type : "success", message : "Campaign has been unflagged !" });
                    this.getCampaigns();
                }
            },
            clearFilters() {
                this.cname = ""
                this.sname = "";
                this.getCampaigns();
            }
        },
        created() {
            this.getCampaigns();
        }
    }
</script>