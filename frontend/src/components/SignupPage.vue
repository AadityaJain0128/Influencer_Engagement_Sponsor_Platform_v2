<template>
    <div id="container">
        <div class="panel">
            <h1 align="center">{{ role[0].toUpperCase().concat(role.substring(1, )) }} Sign Up</h1>
            <br><br>
            <form @submit.prevent="validate">
                <label for="role" class="form-label">Select Role</label>
                <select id="role" name="role" class="form-control" v-model="role">
                    <option value="influencer">Influencer</option>
                    <option value="sponsor">Sponsor</option>
                </select>
                <br>
                <div id="influencer" v-if="role == 'influencer'">
                    <label for="full_name" class="form-label">Full Name</label>
                    <input type="text" id="full_name" name="full_name" v-model="full_name" class="form-control">
                    <br>
                    <label for="niche" class="form-label">Niche</label>
                     <select id="niche" name="niche" class="form-control" v-model="niche">
                        <option v-for="category in categories" :value="category.name" :key="category.id">{{ category.name }}</option>
                     </select>
                </div>
                <div id="sponsor" v-else>
                    <label for="company_name" class="form-label">Company Name</label>
                    <input type="text" id="company_name" name="company_name" v-model="company_name" class="form-control">
                    <br>
                    <label for="industry" class="form-label">Industry</label>
                    <select id="industry" name="industry" class="form-control" v-model="industry">
                        <option v-for="category in categories" :value="category.name" :key="category.id">{{ category.name }}</option>
                     </select>
                </div>
                <br>
                <label for="email" class="form-label">E-Mail ID</label>
                <input type="email" id="email" name="email" v-model="email" class="form-control" required>
                <br>
                <label for="username" class="form-label">Username</label>
                <input type="text" id="username" name="username" v-model="username" class="form-control" required>
                <br>
                <label for="password" class="form-label">Password</label>
                <input type="password" id="password" name="password" class="form-control" minlength="8" v-model="password" required>
                <br>
                <label for="cpassword" class="form-label">Confirm Password</label>
                <input type="password" id="cpassword" name="cpassword" v-model="cpassword" class="form-control">
                <br><br>
                <button type="submit" class="btn btn-dark">Sign Up</button>
                <span style="margin-left: 35vh;">Already have an account? <router-link to="/login">Log In</router-link></span>
            </form>
        </div>
    </div>
</template>


<script>
    export default {
        name : "SignupPage",
        data() {
            return {
                role : "influencer",
                categories : [],
                full_name : "",
                niche : "",
                company_name : "",
                industry : "",
                email : "",
                username : "",
                password : "",
                cpassword : "",
            }
        },
        methods : {
            async fetchCategory() {
                let response = await this.$http.get("/auth/categories");
                this.categories = response.data;
            },

            async validate() {
                if (this.password != this.cpassword) {
                    this.$store.commit("showAlert", { type : "warning", message : "Passwords do not match !" });
                    return;
                }

                let payload = {
                    username : this.username,
                    email : this.email,
                    password : this.password,
                    role : this.role
                }

                if (this.role == "influencer") {
                    payload.full_name = this.full_name;
                    payload.niche = this.niche;
                } else {
                    payload.company_name = this.company_name;
                    payload.industry = this.industry;
                }

                let response = await this.$http.post("/auth/signup", payload);

                if (response.data.status == "success") {
                    this.$store.commit("showAlert", { type : "success", message : "Account created successfully !" });
                    this.$router.push("/login");
                } else {
                    this.$store.commit("showAlert", { type : "error", message : response.data.error });
                }
            }
        },
        created() {
            if (this.$store.state.auth.authToken) {
                this.$store.commit("showAlert", { "type" : "warning", message : "You have already Logged In !" })
                this.$router.push("/");
            }
            this.fetchCategory();
        }
    }
</script>


<style>
    .panel {
        border: 4px solid black;
        border-radius: 10px;
        width: 50%;
        padding: 50px;
        margin: auto;
        margin-top: 40px;
    }

    #container {
        margin: 20px;
        margin-top: 10px;
    }
</style>