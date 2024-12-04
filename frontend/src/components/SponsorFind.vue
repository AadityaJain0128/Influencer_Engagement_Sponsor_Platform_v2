<template>
    <div id="container">
        <h1 align="center">Find Influencers</h1>
        <br><br>
        <div style="width: 20%; float: left;" class="m-3">
            <h3>Filters</h3>
            <br>
            <label for="name" class="form-label">Username / Name</label>
            <input type="text" id="name" name="name" placeholder="Search by Name" v-model="uname" class="form-control">
            <br>
            <label for="niche" class="form-label">Niche</label>
            <select id="niche" name="niche" v-model="niche" class="form-control">
                <option value="">Select Niche</option>
                <option v-for="c in categories" :key="c.name" :value="c.name">{{ c.name }}</option>
            </select>
            <br>
            <button @click="getData" class="btn btn-outline-dark">Search</button>
        </div>
        <div style="width: 65%; float: right;" class="me-5">
            <div v-if="influencers.length > 0" class="row">
                <div v-for="i in influencers" :key="i.id" class="col-md-4 mb-5">
                    <div class="card" style="width: 18rem; align-items: center; text-align: center;">
                        <img :src="SERVER + '/static/' + i.profile_picture" width="200px" height="200px" class="card-title mt-2" style="border-radius: 50%; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title">{{ i.name }}</h5>
                            <p class="card-text">@{{ i.username }}</p>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">Niche: {{ i.niche }}</li>
                            <li v-if="i.avg_rating.length == 0" class="list-group-item">Rating: N/A <span class="text-muted" style="font-size: smaller;">(0)</span></li>
                            <li v-else class="list-group-item">Rating: {{ i.avg_rating[0] }} <span class="text-muted" style="font-size: smaller;">({{ i.avg_rating[1] }})</span></li>
                            <li class="list-group-item">Reach: {{ i.reach }}</li>
                            <li class="list-group-item">
                                Active Socials<br>
                                <span v-if="i.reach == 0" class="text-muted">No Socials added !</span>
                                <span v-else>
                                    <img v-for="[social, ] in Object.entries(fixSocials(i.socials))"  :key="social" :src="'/images/' + social + '.png'" width="30px" class="m-1 mt-2">
                                </span>
                            </li>
                        </ul>
                        <div class="card-body">
                            <button type="button" class="btn btn-outline-dark" data-bs-toggle="modal" :data-bs-target="'#' + i.id">Send Request</button>
                            <div class="modal fade" :id="i.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-lg">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Request @{{ i.username }}</h1>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <table class="table table-striped mt-5">
                                                <tr>
                                                    <th>Messages</th>
                                                    <td><input type="text" name="messages" v-model="messages[i.id]" class="form-control" required></td>
                                                </tr>
                                                <tr>
                                                    <th>Requirements</th>
                                                    <td><input type="text" name="requirements" v-model="requirements[i.id]" class="form-control" required></td>
                                                </tr>
                                                <tr>
                                                    <th>Select Campaign</th>
                                                    <td>
                                                        <select name="campaign_id" class="form-control" v-model="campaign_id" required>
                                                            <option value="" selected disabled>Select Campaign</option>
                                                            <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">{{ campaign.name }}</option>
                                                        </select>
                                                    </td>
                                                </tr>
                                            </table>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                            <button v-if="campaigns.length > 0" @click="send_request(i.id)" class="btn btn-primary">Send Request</button>
                                            <router-link v-else to="/campaigns" class="btn btn-primary">Add a Campaign First !</router-link>
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
        name : "SponsorFind",
        data() {
            return {
                SERVER : "http://127.0.0.1:5000/",
                campaigns : [],
                influencers : [],
                messages : {},
                requirements : {},
                uname : "",
                niche : "",
                categories : [],
                campaign_id : ""
            }
        },
        methods : {
            async getCategory() {
                let { data } = await this.$http.get("/auth/categories");
                this.categories = data;
            },

            async getData() {
                let { data } = await this.$http.get("/sponsor/find", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` },
                    params : { name : this.uname, niche : this.niche }
                });

                if (data.status == "success") {
                    this.campaigns = data.campaigns;
                    this.influencers = data.influencers;

                    if (this.influencers.length > 0) {
                        this.influencers.forEach(i => {
                            this.$set(this.messages, i.id, "");
                            this.$set(this.requirements, i.id, "");
                        });
                    }
                }
            },
            async send_request(id) {
                let { data } = await this.$http.post("/sponsor/send_request",
                    { influencer_id : id, campaign_id : this.campaign_id, messages : this.messages[id], requirements : this.requirements[id] },
                    { headers : { Authorization : `Bearer ${this.$store.getters.authToken}` } }
                );

                let type = data.status == "fail" ? "warning" : "success";
                this.$store.commit("showAlert", { type : type, message : data.message });

                this.$set(this.messages, id, "");
                this.$set(this.requirements, id, "");
            },
            clearFilters() {
                this.uname = "";
                this.niche = "";
                this.getData();
            },
            fixSocials(socials) {
                return Object.entries(socials).filter(([, followers]) => followers > 0).reduce((acc, [social, followers]) => {
                    acc[social] = followers;
                    return acc;
                }, {});
            }
        },
        created() {
            this.getCategory();
            this.getData();
        }
    }
</script>