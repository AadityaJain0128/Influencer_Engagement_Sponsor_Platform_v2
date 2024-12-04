<template>
    <div class="container">
        <div class="m-5">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th colspan="2" class="text-center"><h1>Profile Page</h1></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th scope="row">Profile Picture</th>
                        <td>
                            <div class="d-flex align-items-center">
                                <div style="float: left; width: 40%;">
                                    <img v-if="previewImage" :src="previewImage" width="100" height="100" style="object-fit: cover; border-radius: 50%;">
                                    <img v-else :src="profile" width="100" height="100" style="object-fit: cover; border-radius: 50%;">
                                    <br>
                                    <input type="file" accept="image/*" name="profile_pic" required class="form-control-file" @change="onFileChange" ref="file">
                                </div>
                                <div style="float: right; width: 60%;">
                                    <button v-if="profile == `${SERVER}static/profile_pictures/dpp.png`" class="btn btn-outline-dark btn-sm" style="margin-top: 5vh;" @click="updateProfile">Add Picture</button>
                                    <button v-else class="btn btn-outline-dark btn-sm" style="margin-top: 3vh;" @click="updateProfile">Change Picture</button>
                                    <br>
                                    <a v-if="profile != `${SERVER}static/profile_pictures/dpp.png`" class="btn btn-outline-dark btn-sm mt-2" @click="removeProfile">Remove Picture</a>
                                </div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">User Name</th>
                        <td>@{{ username }}</td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="email">E-Mail ID</label></th>
                        <td>{{ email }}</td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="name">Name</label></th>
                        <td><input type="text" id="name" name="name" v-model="name" class="form-control" required></td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="niche">Industry</label></th>
                        <td>
                            <select id="niche" name="niche" class="form-control" v-model="industry">
                                <option v-for="c in categories" :value="c.name" :key="c.id" :selected="industry == c">{{ c.name }}</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th></th>
                        <td colspan="2">
                            <button class="btn btn-outline-dark" @click="saveChanges">Save Changes</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script>
    export default {
        name : "SponsorProfile",
        data() {
            return {
                name : "",
                industry : "",
                categories : [],
                SERVER : "http://127.0.0.1:5000/",
                file : null,
                previewImage : null
            }            
        },

        methods : {
            async fetchCategory() {
                let response = await this.$http.get("/auth/categories");
                this.categories = response.data;
            },

            async saveChanges() {
                let { data } = await this.$http.put("/sponsor/profile_update", 
                    { name : this.name, industry : this.industry },
                    { headers : { Authorization : `Bearer ${this.$store.getters.authToken}` } }
                );
                if (data.status == "success") {
                    this.$store.commit("setInfo", { id : this.id, name : data.name, category : data.industry, reach : "", socials : "" });
                    this.$store.commit("showAlert", { type : "success", message : data.message });
                }
            },

            onFileChange(event) {
                this.file = event.target.files[0];
                this.previewImage = URL.createObjectURL(this.file);
            },

            async updateProfile() {
                if (!this.file) {
                    return;
                }
                let formData = new FormData();
                formData.append("profile", this.file);
                let { data } = await this.$http.put("/auth/profile_image_update", formData, {
                    headers : { 
                        Authorization : `Bearer ${this.$store.getters.authToken}`,
                        "Content-Type" : "multipart/form-data"
                    },
                });
                if (data.status == "success") {
                    this.$store.commit("setProfileImage", `${this.SERVER}static/${data.url}?date=${Date.now()}`);
                }
                this.$store.commit("showAlert", { type : data.status, message : data.message });
                this.$refs.file.value = null;
                this.file = null;
                this.previewImage = null;
            },

            async removeProfile() {
                let { data } = await this.$http.delete("/auth/profile_image_update", {
                    headers : { Authorization : `Bearer ${this.$store.getters.authToken}`, }
                });
                if (data.status == "success") {
                    this.$store.commit("setProfileImage", `${this.SERVER}static/${data.url}?date=${Date.now()}`);
                }
                this.$store.commit("showAlert", { type : data.status, message : data.message });
                this.$refs.file.value = null;
                this.file = null;
                this.previewImage = null;
            }
        },

        computed : {
            id() { return this.$store.state.auth.id; },
            username() { return this.$store.state.auth.username; },
            role() { return this.$store.state.auth.role; },
            email() { return this.$store.state.auth.email; },
            profile() { return this.$store.state.auth.profile; }
        },

        created() {
            this.fetchCategory();
            this.name = this.$store.state.info.name;
            this.industry = this.$store.state.info.category;
            this.socials = this.$store.state.info.socials;
        }
    }
</script>