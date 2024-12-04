<template>
    <div id="container">
        <div class="panel">
            <h1 align="center">Login</h1>
            <br><br>
            <form @submit.prevent="handleLogin">
                <label for="username" class="form-label">Username</label>
                <input type="text" id="username" name="username" value="" class="form-control" v-model="username" required>
                <br>
                <label for="password" class="form-label">Password</label>
                <input type="password" id="password" name="password" class="form-control" v-model="password" required>
                <br><br>
                <button type="submit" class="btn btn-dark">Login</button>
                <span style="margin-left: 45vh;">New User? <router-link to="/signup">Sign Up</router-link></span>
            </form>
        </div>
    </div>
</template>


<script>
export default {
    name : "LoginPage",
    data() {
        return {
            username : "",
            password : ""
        }
    },
    methods : {
        async handleLogin() {
            let response = await this.$http.post("/auth/login", { "username" : this.username, "password" : this.password });

            if (response.data.status == "success") {
                this.$store.commit("showAlert", { type : "success", message : "Login Successful !" });
                this.$store.commit("setAuth", { role : response.data.role, authToken : response.data.authToken, username : response.data.username, email : response.data.email });
                this.$store.dispatch("fetchProfileImage", this);
                this.$router.push("/dashboard");
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
    }
}
</script>


<style scoped>
    .panel {
        border: 4px solid black;
        border-radius: 10px;
        width: 50%;
        padding: 50px;
        margin: auto;
    }

    #container {
        margin: 20px;
        margin-top: 85px;
    }
</style>