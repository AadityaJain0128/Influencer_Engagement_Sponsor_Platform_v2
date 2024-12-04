<template>
    <div id="container">
        <h1 align="center">Verify Sponsors</h1>
        <br><br>
        <div style="width: 20%; float: left;" class="m-3">
            <h3>Filters</h3>
            <br>
            <label for="name" class="form-label">Username</label>
            <input type="text" id="username" name="username" placeholder="Search by UserName" v-model="uname" class="form-control">
            <br>
            <button @click="getSponsors" class="btn btn-outline-dark">Search</button>
        </div>
        <div style="width: 65%; float: right;" class="me-5">
            <div v-if="sponsors.length > 0" class="row">
                <div v-for="s in sponsors" :key="s.id" class="col-md-4 mb-5">
                    <div class="card" style="width: 18rem; align-items: center; text-align: center;">
                        <img :src="SERVER + '/static/' + s.profile_picture" width="200px" height="200px" class="mt-2" style="border-radius: 50%; object-fit: cover;" loading="lazy">
                        <div class="card-body">
                            <h5 class="card-title">{{ s.name }}</h5>
                            <p class="card-text">@{{ s.username }}</p>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">Industry: {{ s.industry }}</li>
                            <li class="list-group-item"><button @click="verifySponsor(s.id)" class="btn btn-outline-primary">Verify</button></li>
                        </ul>
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
        name : "AdminVerify",
        data() {
            return {
                sponsors : [],
                uname : "",
                SERVER : "http://127.0.0.1:5000"
            }
        },
        methods : {
            async getSponsors() {
                let { data } = await this.$http.get("/admin/sponsors", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` },
                    params : { username : this.uname }
                });

                this.sponsors = data.sponsors;
            },

            async verifySponsor(id) {
                let { data } = await this.$http.post("/admin/verify", 
                    { id : id },
                    { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } }
                );

                if (data.status == "success") {
                    this.$store.commit("showAlert", { type : "success", message : "Sponsor Verified !" });
                    this.getSponsors();
                }
            },

            clearFilters() {
                this.uname = "";
                this.getSponsors();
            }
        },
        created() {
            this.getSponsors();
        }
    }
</script>