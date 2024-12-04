<template>
    <div id="container">
        <h1 align="center">Flagged Users</h1>
        <br><br>
        <div style="width: 20%; float: left;" class="m-3">
            <h3>Filters</h3>
            <br>
            <label for="name" class="form-label">Username</label>
            <input type="text" id="username" name="username" placeholder="Search by UserName" v-model="uname" class="form-control">
            <br>
            <label for="role" class="form-label">Role</label>
            <select id="role" name="role" class="form-control" v-model="role">
                <option value="">All</option>
                <option value="influencer">Influencer</option>
                <option value="sponsor">Sponsor</option>
            </select>
            <br>
            <button @click="getUsers" class="btn btn-outline-dark">Search</button>
        </div>
        <div style="width: 65%; float: right;" class="me-5">
            <div v-if="users.length > 0" class="row">
                <div v-for="user in users" :key="user.username" class="col-md-4 mb-5">
                    <div class="card" style="width: 18rem; align-items: center; text-align: center;">
                        <img :src="SERVER + '/static/' + user.profile_picture" width="200px" height="200px" class="card-title mt-2" style="border-radius: 50%; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title">@{{ user.username }}</h5>
                            <p class="card-text">{{ user.email }}</p>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">Role: {{ user.role.charAt(0).toUpperCase() + user.role.substring(1, ) }}</li>
                        </ul>
                        <div class="card-body">
                            <button @click="unflagUser(user.username)" type="submit" class="btn btn-outline-success">UnFlag User</button>
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
        name : "AdminFindUsers",
        data() {
            return {
                SERVER : "http://127.0.0.1:5000",
                uname : "",
                role : "",
                users : []
            }
        },
        methods : {
            async getUsers() {
                let { data } = await this.$http.get("/admin/flagged_users", {
                    headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` },
                    params : { uname : this.uname, role : this.role }
                });
                if (data.status == "success") {
                    this.users = data.users;
                }
            },
            async unflagUser(username) {
                let { data } = await this.$http.post("/admin/flagged_users",
                    { username : username },
                    { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } }
                );
                if (data.status == "success") {
                    this.$store.commit("showAlert", { type : "success", message : "User has been unflagged !" });
                    this.getUsers();
                }
            },
            clearFilters() {
                this.uname = ""
                this.role = "";
                this.getUsers();
            }
        },
        created() {
            this.getUsers();
        }
    }
</script>