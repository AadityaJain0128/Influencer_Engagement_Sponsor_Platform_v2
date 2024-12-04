<template>
    <div id="container">
        <div class="panel">
            <h1 align="center">Payment Gateway</h1>
            <br>
            <div id="id">
                <label for="upi_id" class="form-label">UPI ID</label>
                <input v-model="upi_id" type="text" id="upi_id" name="upi_id" class="form-control">
                <br>
                <button @click="verifyUPI" class="btn btn-outline-dark">Verify UPI</button>
            </div>
            <br><br>
            <div id="pin" style="display: block;">
                <label for="upi_pin" class="form-label">PIN</label>
                <input v-model="upi_pin" type="number" id="upi_pin" name="upi_pin" class="form-control">
                <br>
                <button @click="markComplete" class="btn btn-outline-dark">Pay</button>
            </div>
        </div>
    </div>
</template>


<script>
    export default {
        name : "PaymentGateway",
        props : ["id"],
        data() {
            return {
                upi_id : "",
                upi_pin : "",
                verify : false
            }
        },
        methods : {
            verifyUPI() {
                if (this.upi_id.includes("@") && this.upi_id.length >= 8) {
                    this.verify = true;
                    this.$store.commit("showAlert", { type : "success", message : "UPI ID validated !" });
                } else {
                    this.$store.commit("showAlert", { type : "error", message : "Enter valid UPI ID !" });
                }
                return;
            },
            async markComplete() {
                if (!this.verify) {
                    this.$store.commit("showAlert", { type : "error", message : "Enter UPI ID first !" });
                    return;
                }
                let { data } = await this.$http.post("/sponsor/campaigns/" + this.id, {},
                { headers : { Authorization : `Bearer ${this.$store.state.auth.authToken}` } });

                if (data.status == "success") {
                    this.$store.commit("showAlert", { type : data.status, message : data.message });
                    this.$router.push("/campaigns/" + this.id);
                }
            }
        }
    }
</script>